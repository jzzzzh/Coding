import math

import torch
import torch.nn as nn


class my_mha(nn.Module):
    """Multi-Head Attention：Q/K/V 投影 -> 多头拆分 -> 注意力 -> 合并输出。"""

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
        # [B, L, d_model] -> [B, n_head, L, head_dim]
        B, L, _ = x.shape
        x = x.reshape(B, L, self.n_head, self.head_dim)
        return x.transpose(1, 2)

    def forward(self, q, k, v, mask=None):
        q = self.split(self.q_proj(q))
        k = self.split(self.k_proj(k))
        v = self.split(self.v_proj(v))

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
    mha = my_mha(d_model=128, n_head=8)
    x = torch.randn(2, 10, 128)
    output, weight = mha(x, x, x)
    print(output.shape)  # [2, 10, 128]
    print(weight.shape)  # [2, 8, 10, 10]
