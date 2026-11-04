import math

import torch
import torch.nn as nn
import torch.nn.functional as F


def half_rotate(x):
    half = x.size(-1) // 2
    return torch.cat([-x[..., half:], x[..., :half]], dim=-1)


class my_rope(nn.Module):
    def __init__(self, max_len, head_dim, base=10000.0):
        super().__init__()
        assert head_dim % 2 == 0
        theta = 1.0 / (base ** (torch.arange(0, head_dim, 2).float() / head_dim))
        pos = torch.arange(max_len).float()
        freqs = torch.outer(pos, theta)
        emb = torch.cat([freqs, freqs], dim=-1)
        self.register_buffer("sin", emb.sin())
        self.register_buffer("cos", emb.cos())

    def forward(self, x):
        seq_len = x.size(-2)
        sin = self.sin[:seq_len].to(dtype=x.dtype)
        cos = self.cos[:seq_len].to(dtype=x.dtype)
        return x * cos + half_rotate(x) * sin


class my_mha_rope(nn.Module):
    def __init__(self, d_model, n_head, max_len=512):
        super().__init__()
        self.d_model = d_model
        self.n_head = n_head
        assert d_model % n_head == 0
        self.head_dim = d_model // n_head
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.rope = my_rope(max_len=max_len, head_dim=self.head_dim)

    def split(self, x):
        B, L, _ = x.shape
        x = x.reshape(B, L, self.n_head, self.head_dim)
        return x.transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        q = self.split(self.q_proj(q))
        k = self.split(self.k_proj(k))
        v = self.split(self.v_proj(v))
        q = self.rope(q)
        k = self.rope(k)
        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.head_dim)
        if mask is not None:
            score = score.masked_fill(mask, float("-inf"))
        weight = torch.softmax(score, dim=-1)
        out = torch.matmul(weight, v).transpose(1, 2).contiguous()
        B, L, _, _ = out.shape
        out = out.reshape(B, L, self.d_model)
        return self.out_proj(out), weight


class TransformerLayer(nn.Module):
    def __init__(self, d_model, n_head, max_len=512):
        super().__init__()
        self.attention = my_mha_rope(d_model, n_head, max_len=max_len)
        self.norm1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        attn_out, weight = self.attention(x, x, x, mask)
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ffn(x))
        return x, weight


class MiniGPT(nn.Module):
    """Embedding -> TransformerLayer(MHA+RoPE) -> LM Head，带 causal mask。"""

    def __init__(self, vocab_size, d_model=128, n_head=4, max_len=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.block = TransformerLayer(d_model, n_head, max_len=max_len)
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, input_ids):
        B, L = input_ids.shape
        x = self.embedding(input_ids)
        mask = torch.triu(
            torch.ones(L, L, dtype=torch.bool, device=x.device),
            diagonal=1,
        )
        x, weight = self.block(x, mask)
        logits = self.lm_head(x)
        return logits, weight


def generate_data(batch_size, seq_len, vocab_size, device):
    # x[t] = (x[t-1] + x[t-2]) % vocab_size
    seq = torch.zeros(batch_size, seq_len + 1, dtype=torch.long, device=device)
    seq[:, 0] = torch.randint(0, vocab_size, (batch_size,), device=device)
    seq[:, 1] = torch.randint(0, vocab_size, (batch_size,), device=device)
    for i in range(2, seq_len + 1):
        seq[:, i] = (seq[:, i - 1] + seq[:, i - 2]) % vocab_size
    return seq[:, :-1], seq[:, 1:]


def train():
    vocab_size, d_model, n_head = 32, 128, 4
    batch_size, seq_len, epochs, lr = 128, 32, 1000, 1e-3
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = MiniGPT(vocab_size, d_model, n_head).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    model.train()

    for step in range(1, epochs + 1):
        input_ids, target_ids = generate_data(batch_size, seq_len, vocab_size, device)
        logits, _ = model(input_ids)
        loss = F.cross_entropy(
            logits[:, 1:, :].reshape(-1, vocab_size),
            target_ids[:, 1:].reshape(-1),
        )
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        if step % 50 == 0:
            with torch.no_grad():
                acc = (logits[:, 1:, :].argmax(dim=-1) == target_ids[:, 1:]).float().mean()
            print(f"Step: {step:4d} | Loss: {loss.item():.4f} | Acc: {acc.item():.4f}")

    return model


if __name__ == "__main__":
    train()
