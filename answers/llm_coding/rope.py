import torch
import torch.nn as nn


def half_rotate(x):
    """把最后一维拆成两半，做 (-x2, x1)。"""
    half = x.size(-1) // 2
    return torch.cat([-x[..., half:], x[..., :half]], dim=-1)


class my_rope(nn.Module):
    """RoPE：按位置对 head_dim 做旋转位置编码，通常只作用在 Q/K 上。"""

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
        # x: [..., seq_len, head_dim]
        seq_len = x.size(-2)
        sin = self.sin[:seq_len].to(dtype=x.dtype)
        cos = self.cos[:seq_len].to(dtype=x.dtype)
        return x * cos + half_rotate(x) * sin


if __name__ == "__main__":
    rope = my_rope(max_len=128, head_dim=64)
    x = torch.randn(2, 8, 10, 64)
    y = rope(x)
    print(y.shape)
    print(torch.allclose(x.norm(dim=-1), y.norm(dim=-1), atol=1e-5))
