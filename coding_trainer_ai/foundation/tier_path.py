from typing import List, Optional, Dict
from coding_trainer_ai.foundation.models import TierLevel, ModuleTier, LearningModule


class TierPathManager:
    """
    Manages progressive 5-Tier learning paths that bridge zero-jargon plain English
    to UK Master's Distinction level rigor.
    """

    def __init__(self):
        self._modules: Dict[str, LearningModule] = self._init_default_modules()

    def _init_default_modules(self) -> Dict[str, LearningModule]:
        modules = {}

        # ----------------------------------------------------------------------
        # Module 1: C++ Pointers & Memory Architecture
        # ----------------------------------------------------------------------
        mod1 = LearningModule(
            id="mod_cpp_memory",
            title="C++ Pointers & Memory Architecture",
            track="Software Engineering & C++",
            description="Bridge from physical archival call numbers to raw pointers, smart pointers, and RAII memory safety.",
        )
        mod1.tiers[TierLevel.TIER_1_FOUNDATION] = ModuleTier(
            tier_level=TierLevel.TIER_1_FOUNDATION,
            title="Tier 1: Archival Call Numbers & Memory Addresses",
            summary="Understanding pointers through physical library call numbers.",
            explanation=(
                "Imagine a rare manuscript stored in a national archive. Instead of copying the 500-page manuscript, "
                "the archive catalog hands you a call number slip: 'Shelf 14, Box 3'. "
                "In computer memory, every variable is stored at a physical memory address. A pointer variable is simply "
                "a slip of paper that holds that memory address."
            ),
            code_or_math_example=(
                "// Mental Model:\n"
                "Manuscript (Value)  = 1648\n"
                "Call Slip (Pointer)  = Address 0x7ffd98a2"
            ),
            uk_distinction_key_takeaway="A pointer is a variable containing a memory address, not the value itself.",
        )
        mod1.tiers[TierLevel.TIER_2_SYNTAX] = ModuleTier(
            tier_level=TierLevel.TIER_2_SYNTAX,
            title="Tier 2: Syntax of Dereferencing & Address-Of Operators",
            summary="Mastering `&` (address-of) and `*` (dereference) operators.",
            explanation=(
                "Use `&` to obtain the memory address of an existing variable. "
                "Use `*` when declaring a pointer variable, and use `*` again in front of a pointer to dereference it "
                "(go to that memory location and read/write the value)."
            ),
            code_or_math_example=(
                "int val = 42;\n"
                "int* pVal = &val;               // & gets address of val\n"
                "std::cout << *pVal << std::endl; // * reads value at pVal (prints 42)\n"
                "*pVal = 100;                    // Modifies val to 100!"
            ),
            uk_distinction_key_takeaway="`&x` yields the memory address of x; `*p` inspects or mutates the object at address p.",
        )
        mod1.tiers[TierLevel.TIER_3_INTERMEDIATE] = ModuleTier(
            tier_level=TierLevel.TIER_3_INTERMEDIATE,
            title="Tier 3: Dynamic Heap Memory Allocation (`new` & `delete`)",
            summary="Allocating dynamic memory on the Heap and preventing memory leaks.",
            explanation=(
                "Stack memory is automatic but fixed in size during function scope. "
                "Heap memory allows allocating dynamic arrays or objects at runtime using `new`. "
                "Every `new` MUST be matched with a corresponding `delete` (or `delete[]` for arrays) to prevent memory leaks."
            ),
            code_or_math_example=(
                "int* arr = new int[5]; // Allocate array of 5 integers on Heap\n"
                "for (int i=0; i<5; ++i) arr[i] = i * 10;\n"
                "delete[] arr;          // Crucial cleanup! Prevents leak."
            ),
            uk_distinction_key_takeaway="Failure to delete heap allocations creates memory leaks; double deletion causes undefined behavior.",
        )
        mod1.tiers[TierLevel.TIER_4_ADVANCED_MSC] = ModuleTier(
            tier_level=TierLevel.TIER_4_ADVANCED_MSC,
            title="Tier 4: RAII & Smart Pointers (`std::unique_ptr`, `std::shared_ptr`)",
            summary="Modern C++ Resource Acquisition Is Initialization (RAII) and smart pointers.",
            explanation=(
                "Modern C++ avoids manual `new`/`delete`. RAII binds resource lifecycle to object lifetime. "
                "`std::unique_ptr` maintains sole ownership and automatically deletes memory when out of scope. "
                "`std::shared_ptr` uses reference counting for shared ownership."
            ),
            code_or_math_example=(
                "#include <memory>\n\n"
                "void process() {\n"
                "    auto ptr = std::make_unique<int>(42); // Safe! Auto-deleted on scope exit.\n"
                "} // Memory automatically freed here without `delete`!"
            ),
            uk_distinction_key_takeaway="`unique_ptr` has zero runtime overhead over raw pointers while guaranteeing exception safety.",
        )
        mod1.tiers[TierLevel.TIER_5_EXAM_DISTINCTION] = ModuleTier(
            tier_level=TierLevel.TIER_5_EXAM_DISTINCTION,
            title="Tier 5: UK MSc Distinction Analysis – Memory Safety & Cache Alignment",
            summary="Evaluating dangling pointers, cache locality, and std::move semantics.",
            explanation=(
                "Exam Distinction questions test edge-case traps: returning pointers to deallocated stack frames, "
                "circular dependencies in `shared_ptr` (requiring `std::weak_ptr`), move semantics vs copying, "
                "and cache misses caused by heap fragmentation."
            ),
            code_or_math_example=(
                "// Distinction Essay / Code Trap:\n"
                "int* bad_func() {\n"
                "    int local_var = 10;\n"
                "    return &local_var; // CRITICAL BUG: Returns address of stack variable freed on return!\n"
                "}"
            ),
            uk_distinction_key_takeaway="Distinction answers critically evaluate move semantics (`std::move`), weak pointers for cyclic graphs, and cache line spatial locality.",
        )
        modules[mod1.id] = mod1

        # ----------------------------------------------------------------------
        # Module 2: Gradient Descent & Machine Learning Optimization
        # ----------------------------------------------------------------------
        mod2 = LearningModule(
            id="mod_grad_descent",
            title="Gradient Descent & Loss Landscapes",
            track="Math for AI & Machine Learning",
            description="From hiking down a foggy mountain to PyTorch autograd computations and non-convex saddle points.",
        )
        mod2.tiers[TierLevel.TIER_1_FOUNDATION] = ModuleTier(
            tier_level=TierLevel.TIER_1_FOUNDATION,
            title="Tier 1: Misty Mountain Expedition Analogy",
            summary="Conceptual understanding of navigating downhill.",
            explanation=(
                "Imagine standing on a foggy mountain peak attempting to reach sea level. "
                "You cannot see the full landscape, but you feel the incline of the ground under your boots. "
                "Taking steps in the steepest downhill direction eventually leads you to the valley floor."
            ),
            code_or_math_example="Goal: Minimize Loss (Altitude) by stepping opposite the Gradient (Slope)",
            uk_distinction_key_takeaway="Gradient descent finds parameters that minimize error by following slope direction.",
        )
        mod2.tiers[TierLevel.TIER_2_SYNTAX] = ModuleTier(
            tier_level=TierLevel.TIER_2_SYNTAX,
            title="Tier 2: 1D Gradient Descent Update Rule",
            summary="Implementing a basic single-parameter gradient step in Python.",
            explanation=(
                "For a single weight w and loss function L(w), the derivative dL/dw gives the slope. "
                "We update w by subtracting learning_rate * slope."
            ),
            code_or_math_example=(
                "# Minimize L(w) = w^2\n"
                "w = 10.0\n"
                "learning_rate = 0.1\n"
                "for _ in range(20):\n"
                "    grad = 2 * w            # Derivative dL/dw = 2*w\n"
                "    w = w - learning_rate * grad\n"
                "print(w)                    # Approaches 0.0!"
            ),
            uk_distinction_key_takeaway="Update equation: w_new = w_old - alpha * (dL/dw).",
        )
        mod2.tiers[TierLevel.TIER_3_INTERMEDIATE] = ModuleTier(
            tier_level=TierLevel.TIER_3_INTERMEDIATE,
            title="Tier 3: Multivariable Gradients & Mean Squared Error (MSE)",
            summary="Extending to vector parameters θ and matrix data inputs X.",
            explanation=(
                "With multiple weights θ, the gradient ∇L(θ) is a vector containing partial derivatives for each weight. "
                "Mean Squared Error measures average squared difference between predictions and targets."
            ),
            code_or_math_example=(
                "import numpy as np\n\n"
                "def mse_loss(y_pred, y_true):\n"
                "    return np.mean((y_pred - y_true) ** 2)\n\n"
                "# Gradient w.r.t weights in linear regression: (2/N) * X^T * (X@w - y)"
            ),
            uk_distinction_key_takeaway="∇L(θ) is a vector of partial derivatives [∂L/∂w1, ∂L/∂w2, ..., ∂L/∂wn]^T.",
        )
        mod2.tiers[TierLevel.TIER_4_ADVANCED_MSC] = ModuleTier(
            tier_level=TierLevel.TIER_4_ADVANCED_MSC,
            title="Tier 4: PyTorch Autograd & Computational Graphs (DAGs)",
            summary="How deep learning frameworks perform automatic differentiation.",
            explanation=(
                "PyTorch constructs a Directed Acyclic Graph (DAG) of tensor operations during the forward pass. "
                "Calling `loss.backward()` executes reverse-mode automatic differentiation using the chain rule."
            ),
            code_or_math_example=(
                "import torch\n\n"
                "w = torch.tensor([2.0], requires_grad=True)\n"
                "loss = w**3 + 5*w\n"
                "loss.backward()              # Computes dLoss/dw = 3*w^2 + 5 = 3(4) + 5 = 17\n"
                "print(w.grad)               # Output: tensor([17.])"
            ),
            uk_distinction_key_takeaway="Reverse-mode automatic differentiation computes gradients for millions of parameters efficiently in O(N) operations.",
        )
        mod2.tiers[TierLevel.TIER_5_EXAM_DISTINCTION] = ModuleTier(
            tier_level=TierLevel.TIER_5_EXAM_DISTINCTION,
            title="Tier 5: UK MSc Distinction Analysis – Non-Convex Landscapes & Saddle Points",
            summary="Critical evaluation of local minima, saddle points, Hessian matrix (H), and Adam optimizer dynamics.",
            explanation=(
                "In high-dimensional neural network loss surfaces, saddle points (where ∇L = 0 but Hessian H has mixed positive/negative eigenvalues) "
                "are far more prevalent than local minima. Distinction answers analyze momentum (Adam/RMSProp) and learning rate schedulers to escape saddle points."
            ),
            code_or_math_example=(
                "Hessian Matrix: H_{ij} = \\frac{\\partial^2 L}{\\partial \\theta_i \\partial \\theta_j}\n"
                "Saddle Point Condition: ∇L = 0 AND det(H) < 0 (Eigenvalues have mixed signs)."
            ),
            uk_distinction_key_takeaway="Distinction essays contrast 1st-order methods (SGD/Adam) with 2nd-order methods (Newton-Raphson/BFGS) under non-convexity.",
        )
        modules[mod2.id] = mod2

        return modules

    def get_all_modules(self) -> List[LearningModule]:
        return list(self._modules.values())

    def get_module_by_id(self, mod_id: str) -> Optional[LearningModule]:
        return self._modules.get(mod_id)
