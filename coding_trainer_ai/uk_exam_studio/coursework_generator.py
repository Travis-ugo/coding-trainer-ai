from coding_trainer_ai.uk_exam_studio.models import LaTeXReportTemplate


class CourseworkReportGenerator:
    """
    Generates publication-ready UK Master's LaTeX Report templates
    and Matplotlib benchmarking code snippets for MSc AI & Robotics coursework.
    """

    def generate_latex_template(
        self, title: str = "Autonomous Robotics & AI System Evaluation", author: str = "UK MSc Candidate"
    ) -> LaTeXReportTemplate:
        abstract_text = (
            "This report critically evaluates the architectural design, algorithmic performance, "
            "and failure modes of autonomous robotics perception and path planning algorithms. "
            "We present empirical benchmarking results comparing BFS, Dijkstra, and A* search across varying obstacle density costmaps."
        )

        sections = {
            "1. Introduction": "Background of the problem, research objectives, and Non-CS intuitive domain mapping.",
            "2. System Architecture": "Component decomposition including ROS 2 Node communication graphs, topic channels, and transformation frames SE(3).",
            "3. Experimental Methodology": "Setup of simulation testbeds, synthetic dataset generation, and execution environment specifications.",
            "4. Results & Benchmarking": "Performance graphs comparing execution latency (ms) and peak RAM usage (MB) across problem scaling.",
            "5. Critical Evaluation & Discussion": "Rigorous evaluation of failure modes, edge case boundary limits, and trade-offs between unimodal EKF and multimodal Particle Filters.",
            "6. Conclusion": "Summary of findings, core takeaways, and recommendations for real-world deployment.",
        }

        full_latex = (
            "\\documentclass[11pt, a4paper]{article}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage{amsmath, amssymb, graphicx, hyperref, booktabs}\n"
            "\\usepackage{geometry}\n"
            "\\geometry{margin=1in}\n\n"
            f"\\title{{{title}}}\n"
            f"\\author{{{author} \\\\ Department of Computer Science & Robotics}}\n"
            "\\date{\\today}\n\n"
            "\\begin{document}\n"
            "\\maketitle\n\n"
            "\\begin{abstract}\n"
            f"{abstract_text}\n"
            "\\end{abstract}\n\n"
            "\\section{1. Introduction}\n"
            "Autonomous navigation requires robust coordination between perception, localization, and motion control...\n\n"
            "\\section{2. System Architecture}\n"
            "The system is implemented as a ROS 2 node graph publishing sensor data over topic channels...\n\n"
            "\\section{3. Experimental Methodology}\n"
            "Experiments were conducted across 100 Monte Carlo simulation runs...\n\n"
            "\\section{4. Results \& Benchmarking}\n"
            "Figure 1 illustrates execution runtime scaled against grid size $N \\times N$...\n\n"
            "\\section{5. Critical Evaluation \& Discussion}\n"
            "While A* search guarantees path optimality given an admissible heuristic $h(n) \\le h^*(n)$, memory consumption scales as $O(b^d)$...\n\n"
            "\\section{6. Conclusion}\n"
            "In conclusion, the proposed architecture meets all operational criteria...\n\n"
            "\\end{document}\n"
        )

        return LaTeXReportTemplate(
            title=title,
            author_background=author,
            abstract=abstract_text,
            sections=sections,
            full_latex_code=full_latex,
        )

    def get_matplotlib_benchmark_code(self) -> str:
        return (
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "# Benchmark data for UK MSc Report\n"
            "grid_sizes = [10, 50, 100, 200, 500]\n"
            "bfs_time_ms = [0.5, 3.2, 14.5, 62.0, 380.0]\n"
            "astar_time_ms = [0.2, 1.1, 4.2, 18.5, 95.0]\n\n"
            "plt.figure(figsize=(8, 5))\n"
            "plt.plot(grid_sizes, bfs_time_ms, 'o--', label='BFS (Uninformed Search)', color='crimson')\n"
            "plt.plot(grid_sizes, astar_time_ms, 's-', label='A* Search (Euclidean Heuristic)', color='navy')\n"
            "plt.xlabel('Grid Map Size (N x N)', fontsize=12)\n"
            "plt.ylabel('Execution Latency (ms)', fontsize=12)\n"
            "plt.title('Path Planning Runtime Performance Comparison', fontsize=14)\n"
            "plt.legend()\n"
            "plt.grid(True, linestyle=':')\n"
            "plt.savefig('benchmark_results.png', dpi=300)\n"
            "print('Saved benchmark plot to benchmark_results.png')"
        )
