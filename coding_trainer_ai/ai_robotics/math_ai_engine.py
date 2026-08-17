import math
from typing import List, Tuple, Dict, Any
from coding_trainer_ai.ai_robotics.models import TransformationMatrix


class MathAIEngine:
    """
    Engine for AI & Robotics mathematical operations:
    - Linear Algebra (Matrix Multiplication, 2D/3D SE(3) Transformations)
    - Calculus (Gradient Descent Loss Step Calculations)
    - Probability (1D Kalman Filter Estimation)
    """

    @staticmethod
    def matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        rows_a = len(a)
        cols_a = len(a[0])
        rows_b = len(b)
        cols_b = len(b[0])

        if cols_a != rows_b:
            raise ValueError(f"Cannot multiply matrix dimensions {rows_a}x{cols_a} and {rows_b}x{cols_b}")

        result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    @staticmethod
    def create_2d_transform_matrix(angle_rad: float, tx: float, ty: float, frame_from: str = "base", frame_to: str = "tool") -> TransformationMatrix:
        """
        Creates a 3x3 SE(2) homogeneous transformation matrix:
        [ cos(θ) -sin(θ)  tx ]
        [ sin(θ)  cos(θ)  ty ]
        [   0       0      1 ]
        """
        cos_t = math.cos(angle_rad)
        sin_t = math.sin(angle_rad)

        matrix_data = [
            [round(cos_t, 4), round(-sin_t, 4), round(tx, 4)],
            [round(sin_t, 4), round(cos_t, 4), round(ty, 4)],
            [0.0, 0.0, 1.0],
        ]
        return TransformationMatrix(matrix_data=matrix_data, frame_from=frame_from, frame_to=frame_to)

    @staticmethod
    def gradient_descent_step(
        weights: List[float], gradients: List[float], learning_rate: float = 0.01
    ) -> List[float]:
        """
        Performs one gradient descent parameter update: θ_new = θ_old - learning_rate * ∇L
        """
        if len(weights) != len(gradients):
            raise ValueError("Weights and gradients vectors must have equal dimensions.")

        return [round(w - learning_rate * g, 4) for w, g in zip(weights, gradients)]

    @staticmethod
    def kalman_filter_1d_step(
        x_estimate: float,
        p_covariance: float,
        measurement: float,
        process_noise: float = 0.1,
        measurement_noise: float = 0.5,
    ) -> Dict[str, float]:
        """
        1D Kalman Filter state estimation:
        1. Predict: x_prior = x_est, P_prior = P + Q
        2. Update: K = P_prior / (P_prior + R)
                   x_post = x_prior + K * (measurement - x_prior)
                   P_post = (1 - K) * P_prior
        """
        # Predict
        x_prior = x_estimate
        p_prior = p_covariance + process_noise

        # Update
        kalman_gain = p_prior / (p_prior + measurement_noise)
        x_post = x_prior + kalman_gain * (measurement - x_prior)
        p_post = (1.0 - kalman_gain) * p_prior

        return {
            "x_estimate": round(x_post, 4),
            "p_covariance": round(p_post, 4),
            "kalman_gain": round(kalman_gain, 4),
        }
