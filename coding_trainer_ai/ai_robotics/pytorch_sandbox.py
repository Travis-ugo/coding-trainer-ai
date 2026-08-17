from typing import List, Dict, Any, Tuple


class SimulatedTensor:
    """
    Simulates a PyTorch Tensor object supporting autograd gradients.
    """

    def __init__(self, data: List[float], requires_grad: bool = False):
        self.data = list(data)
        self.requires_grad = requires_grad
        self.grad: List[float] = [0.0] * len(data) if requires_grad else []

    def shape(self) -> Tuple[int, ...]:
        return (len(self.data),)

    def dot(self, other: "SimulatedTensor") -> float:
        if len(self.data) != len(other.data):
            raise ValueError("Tensor dimension mismatch for dot product.")
        return sum(a * b for a, b in zip(self.data, other.data))

    def __repr__(self) -> str:
        return f"tensor({self.data}, requires_grad={self.requires_grad})"


class PyTorchSandbox:
    """
    Simulates PyTorch Tensor operations, linear layers, MSE loss, and autograd backpropagation.
    """

    @staticmethod
    def linear_forward(x: SimulatedTensor, w: SimulatedTensor, b: float) -> float:
        """
        Calculates linear layer forward pass: y = x · w + b
        """
        return x.dot(w) + b

    @staticmethod
    def mse_loss(prediction: float, target: float) -> float:
        """
        Calculates Mean Squared Error: L = (prediction - target)^2
        """
        return (prediction - target) ** 2

    @staticmethod
    def autograd_backward(
        x: SimulatedTensor, w: SimulatedTensor, b: float, target: float
    ) -> Dict[str, Any]:
        """
        Simulates PyTorch `loss.backward()` reverse-mode automatic differentiation:
        Forward: y = x · w + b, Loss = (y - target)^2
        Backward: dL/dy = 2 * (y - target)
                  dL/dw_i = (dL/dy) * (dy/dw_i) = 2 * (y - target) * x_i
                  dL/db   = (dL/dy) * (dy/db)   = 2 * (y - target) * 1
        """
        y_pred = PyTorchSandbox.linear_forward(x, w, b)
        loss = PyTorchSandbox.mse_loss(y_pred, target)

        d_loss_dy = 2.0 * (y_pred - target)
        d_loss_dw = [d_loss_dy * xi for xi in x.data]
        d_loss_db = d_loss_dy * 1.0

        if w.requires_grad:
            w.grad = [round(g, 4) for g in d_loss_dw]

        return {
            "prediction": round(y_pred, 4),
            "loss": round(loss, 4),
            "grad_w": [round(g, 4) for g in d_loss_dw],
            "grad_b": round(d_loss_db, 4),
        }
