import math

import torch
import torch.nn as nn


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
    """Multi-Head Attention + RoPE（只旋转 Q/K）。"""

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
        out = torch.matmul(weight, v)
        out = out.transpose(1, 2).contiguous()
        B, L, _, _ = out.shape
        out = out.reshape(B, L, self.d_model)
        out = self.out_proj(out)
        return out, weight


if __name__ == "__main__":
    mha = my_mha_rope(d_model=128, n_head=8)
    x = torch.randn(2, 10, 128)
    output, weight = mha(x, x, x)
    print(output.shape)  # [2, 10, 128]
    print(weight.shape)  # [2, 8, 10, 10]
