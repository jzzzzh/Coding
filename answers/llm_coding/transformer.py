import math

import torch
import torch.nn as nn


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_head):
        super().__init__()
        self.d_model = d_model
        self.n_head = n_head
        assert d_model % n_head == 0
        self.head_dim = d_model // n_head
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def split(self, x):
        B, L, _ = x.shape
        return x.reshape(B, L, self.n_head, self.head_dim).transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        q, k, v = self.split(self.q_proj(q)), self.split(self.k_proj(k)), self.split(self.v_proj(v))
        score = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(self.head_dim)
        if mask is not None:
            score = score.masked_fill(mask, float("-inf"))
        weight = torch.softmax(score, dim=-1)
        out = torch.matmul(weight, v).transpose(1, 2).contiguous()
        B, L, _, _ = out.shape
        return self.out_proj(out.reshape(B, L, self.d_model)), weight


class EncoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ff=512):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_head)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.ReLU(), nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        attn_out, _ = self.self_attn(x, x, x, mask)
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ffn(x))
        return x


class DecoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ff=512):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_head)
        self.cross_attn = MultiHeadAttention(d_model, n_head)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.ReLU(), nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)

    def forward(self, x, memory, self_mask=None, cross_mask=None):
        attn_out, _ = self.self_attn(x, x, x, self_mask)
        x = self.norm1(x + attn_out)
        cross_out, _ = self.cross_attn(x, memory, memory, cross_mask)
        x = self.norm2(x + cross_out)
        x = self.norm3(x + self.ffn(x))
        return x


class Transformer(nn.Module):
    """
    最简 Encoder-Decoder Transformer：
        src -> Embedding -> Encoder
        tgt -> Embedding -> Decoder(memory) -> Linear -> logits
    """

    def __init__(
        self,
        src_vocab_size,
        tgt_vocab_size,
        d_model=128,
        n_head=8,
        n_layer=2,
        d_ff=512,
        max_len=512,
        pad_id=0,
    ):
        super().__init__()
        self.pad_id = pad_id
        self.src_embed = nn.Embedding(src_vocab_size, d_model, padding_idx=pad_id)
        self.tgt_embed = nn.Embedding(tgt_vocab_size, d_model, padding_idx=pad_id)
        self.pos_embed = nn.Embedding(max_len, d_model)
        self.encoder_layers = nn.ModuleList(
            [EncoderLayer(d_model, n_head, d_ff) for _ in range(n_layer)]
        )
        self.decoder_layers = nn.ModuleList(
            [DecoderLayer(d_model, n_head, d_ff) for _ in range(n_layer)]
        )
        self.lm_head = nn.Linear(d_model, tgt_vocab_size)

    def add_pos(self, x):
        L = x.size(1)
        pos = torch.arange(L, device=x.device)
        return x + self.pos_embed(pos)

    def forward(self, src_ids, tgt_ids):
        src = self.add_pos(self.src_embed(src_ids))
        tgt = self.add_pos(self.tgt_embed(tgt_ids))

        for layer in self.encoder_layers:
            src = layer(src)

        L = tgt_ids.size(1)
        causal_mask = torch.triu(
            torch.ones(L, L, dtype=torch.bool, device=tgt.device), diagonal=1
        )
        for layer in self.decoder_layers:
            tgt = layer(tgt, src, self_mask=causal_mask)

        return self.lm_head(tgt)


if __name__ == "__main__":
    model = Transformer(src_vocab_size=100, tgt_vocab_size=100)
    src = torch.randint(1, 100, (2, 10))
    tgt = torch.randint(1, 100, (2, 7))
    logits = model(src, tgt)
    print(logits.shape)  # [2, 7, 100]
