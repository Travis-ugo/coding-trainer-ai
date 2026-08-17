from typing import List, Optional, Dict
from coding_trainer_ai.foundation.models import MathNotationCard


class MathRosettaStone:
    """
    Rosetta Stone decoder for AI & Robotics mathematical notation, Greek symbols,
    and equation derivations for non-math backgrounds.
    """

    def __init__(self):
        self._cards: List[MathNotationCard] = self._init_default_cards()
        self._greek_alphabet: Dict[str, str] = self._init_greek_alphabet()

    def _init_greek_alphabet(self) -> Dict[str, str]:
        return {
            "α (Alpha)": "Learning rate / step size in gradient descent algorithms.",
            "β (Beta)": "Momentum coefficient or smoothing parameter in optimizers (Adam).",
            "γ (Gamma)": "Discount factor in Reinforcement Learning (0 <= γ < 1).",
            "δ (Delta)": "Difference or error term (e.g. TD error in RL, perturbation).",
            "θ (Theta)": "Model parameters/weights vector in neural networks L(θ).",
            "λ (Lambda)": "Regularization strength penalty (L1/L2 ridge/lasso penalty).",
            "μ (Mu)": "Mean (average) of a probability distribution or dataset.",
            "σ (Sigma)": "Standard deviation OR Sigmoid activation function σ(z) = 1/(1+e^-z).",
            "τ (Tau)": "Joint torque in robotics dynamics OR target network update rate.",
            "ω (Omega)": "Angular velocity (rotational speed rad/s in robotics kinematics).",
            "∇ (Nabla)": "Gradient vector operator (multivariable derivative of steepest increase).",
            "Σ (Capital Sigma)": "Summation operator over an index (adds numbers in a loop).",
            "Π (Capital Pi)": "Product operator over an index (multiplies numbers in a loop).",
        }

    def _init_default_cards(self) -> List[MathNotationCard]:
        return [
            MathNotationCard(
                id="math_001",
                symbol="∇L(θ)",
                name="Gradient of Loss Vector",
                domain="Calculus & Optimization (Machine Learning)",
                plain_english_breakdown=(
                    "The gradient vector ∇L(θ) points in the direction where the loss (error) increases "
                    "most steeply. To train a model, we step in the OPPOSITE direction (-∇L) to reduce error."
                ),
                variable_roles={
                    "∇ (Nabla)": "Gradient operator (calculates partial derivatives along all dimensions)",
                    "L": "Loss Function (measures how wrong the model predictions are)",
                    "θ (Theta)": "Model weights/parameters being adjusted",
                },
                msc_application="Used in every PyTorch/TensorFlow backpropagation step to update neural network weights.",
                latex_example="\\theta_{new} = \\theta_{old} - \\alpha \\cdot \\nabla L(\\theta)",
            ),
            MathNotationCard(
                id="math_002",
                symbol="∑_{i=1}^n x_i",
                name="Capital Sigma Summation Loop",
                domain="Foundation Math & Statistics",
                plain_english_breakdown=(
                    "Capital Sigma is simply a mathematical 'for loop'. It means start at counter i = 1, "
                    "evaluate x_i, and add it to a running total until you reach i = n."
                ),
                variable_roles={
                    "∑": "Summation symbol (start loop and add elements)",
                    "i=1": "Loop initialization counter (start at 1)",
                    "n": "Upper bound (stop after index n)",
                    "x_i": "The variable element at step i",
                },
                msc_application="Found in loss functions (MSE), vector dot products, and mean calculations.",
                latex_example="\\bar{x} = \\frac{1}{n} \\sum_{i=1}^{n} x_i",
            ),
            MathNotationCard(
                id="math_003",
                symbol="J ∈ ℝ^{m × n}",
                name="Jacobian Matrix",
                domain="Linear Algebra & Robotics Kinematics",
                plain_english_breakdown=(
                    "The Jacobian is a matrix of partial derivatives that maps how changes in robot joint angles "
                    "(inputs n) produce velocity changes at the robot's end-effector hand (outputs m)."
                ),
                variable_roles={
                    "J": "Jacobian matrix",
                    "∈ (in)": "Element of / belongs to",
                    "ℝ": "Real numbers",
                    "m × n": "Dimensions: m rows (output velocities) by n columns (input joint rates)",
                },
                msc_application="Crucial for Robot Arm Inverse Kinematics (calculating how joints move to reach a cup).",
                latex_example="\\mathbf{\\dot{x}} = \\mathbf{J}(\\mathbf{q}) \\mathbf{\\dot{q}}",
            ),
            MathNotationCard(
                id="math_004",
                symbol="E_{x ~ p}[f(x)]",
                name="Expected Value / Expectation",
                domain="Probability & Statistics for AI",
                plain_english_breakdown=(
                    "The long-term average outcome of evaluating function f(x) when input x is randomly "
                    "sampled according to probability distribution p(x)."
                ),
                variable_roles={
                    "E": "Expectation / Expected Value operator (weighted average)",
                    "x ~ p": "Variable x drawn from probability distribution p",
                    "f(x)": "The function or reward calculated at x",
                },
                msc_application="Core equation in Reinforcement Learning (expected future reward) and Variational Autoencoders (VAEs).",
                latex_example="\\mathbb{E}_{x \\sim p}[f(x)] = \\int p(x) f(x) dx",
            ),
        ]

    def get_all_cards(self) -> List[MathNotationCard]:
        return self._cards

    def get_greek_alphabet(self) -> Dict[str, str]:
        return self._greek_alphabet

    def decode_symbol(self, query: str) -> List[MathNotationCard]:
        query_lower = query.lower()
        results = []
        for card in self._cards:
            if (
                query_lower in card.symbol.lower()
                or query_lower in card.name.lower()
                or query_lower in card.domain.lower()
                or query_lower in card.plain_english_breakdown.lower()
            ):
                results.append(card)
        return results
