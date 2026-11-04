import torch
import torch.nn as nn


class my_layernorm(nn.Module):
    """
    LayerNorm: 对最后一维做 (x - mean) / sqrt(var + eps) * gamma + beta
    """

    def __init__(self, normalized_shape, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.gamma = nn.Parameter(torch.ones(normalized_shape))
        self.beta = nn.Parameter(torch.zeros(normalized_shape))

    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        x_hat = (x - mean) / torch.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta


if __name__ == "__main__":
    ln = my_layernorm(8)
    x = torch.randn(2, 4, 8)
    y = ln(x)
    print(y.shape)
    print(y.mean(dim=-1))  # 约 0
    print(y.std(dim=-1))   # 约 1
