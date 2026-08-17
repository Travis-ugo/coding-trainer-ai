import os
import sys
import math
import time
import random
from coding_trainer_ai.python_trainer import PythonCurriculum, PracticeEngine, QuestionType
from coding_trainer_ai.quiz_engine import (
    DynamicQuizGenerator,
    QuizManager,
    QuestionCategory,
    QuestionTimer,
)
from coding_trainer_ai.ai_engine import GeminiAIEngine
from coding_trainer_ai.analytics_studio import (
    GradeAnalyticsEngine,
    DailyRoutineGenerator,
    WebStudioServer,
)
from coding_trainer_ai.uk_exam_studio import (
    UKExamEngine,
    CourseworkReportGenerator,
    SocraticTutor,
    ExamSection,
)
from coding_trainer_ai.dsa_track import (
    DSARepository,
    WhiteboardEvaluator,
    WhiteboardSubmission,
    DSAPattern,
)
from coding_trainer_ai.ai_robotics import (
    MathAIEngine,
    PyTorchSandbox,
    SimulatedTensor,
    VirtualROS2Sandbox,
    SpecializedTrack,
)
from coding_trainer_ai.syntax_drills import (
    AntiCopilotEngine,
    NoCompilerExamMode,
    DrillBank,
    DrillType,
)
from coding_trainer_ai.srs import DeckRepository, ReviewRating
from coding_trainer_ai.ingestion import (
    DocDownloader,
    DocParser,
    MultiFormatParser,
    AutoCurriculumGenerator,
)
from coding_trainer_ai.foundation import AnalogyEngine, MathRosettaStone, TierPathManager


USER_UPLOADS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "resources",
    "user_uploads",
)


def print_banner():
    ai_engine = GeminiAIEngine()
    ai_status = "✨ Live Gemini AI Active" if ai_engine.config.is_active else "⚡ Offline Mode (Press K to add Gemini API key)"

    print("\n" + "=" * 72)
    print(" 🧠  CODING TRAINER AI - Master's Studio & Gemini AI Engine")
    print(" 🎓  Bridging Non-CS Backgrounds to Master's Degree Distinction")
    print("=" * 72)
    print(f" Status: {ai_status}")
    print(" Active learning: Gemini Socratic Tutor, UK exam simulator,")
    print(" real-time timers, grade heatmaps, Virtual ROS 2, SM-2 SRS.")
    print("-" * 72)
    print(" Master's Degree Marking Scale:")
    print("   🏆 Distinction : 70% - 100%")
    print("   📜 Merit       : 60% - 69%")
    print("   ✅ Pass        : 50% - 59% (Minimum threshold to unlock next level)")
    print("   ❌ Fail        :  0% - 49% (Retake required)")
    print("-" * 72)


def configure_gemini_api_key():
    ai_engine = GeminiAIEngine()
    print("\n" + "=" * 60)
    print(" 🔑 CONFIGURE GEMINI AI API KEY")
    print("=" * 60)
    current_key = "Loaded (Active)" if ai_engine.config.is_active else "None (Offline Heuristics)"
    print(f" Current Gemini API Key Status: {current_key}")
    print(" Enter your Gemini API key to unlock Live Socratic Tutoring,")
    print(" AI Exam Essay Evaluation, and Dynamic Question Generation.")
    print("-" * 60)
    new_key = input("Enter Gemini API Key (or press Enter to keep current): ").strip()
    if new_key:
        ai_engine.set_api_key(new_key)
        print("\n ✅ Gemini API Key saved successfully! Live AI Engine is NOW ACTIVE.")
    else:
        print("\n Kept current configuration.")
    print("=" * 60)
    input("\nPress Enter to return...")


def run_analytics_studio_hub():
    analytics_engine = GradeAnalyticsEngine()
    routine_gen = DailyRoutineGenerator()
    web_studio = WebStudioServer()
    quiz_manager = QuizManager()

    while True:
        print("\n" + "=" * 60)
        print(" 💻 GRADE ANALYTICS, DAILY ROUTINE & WEB STUDIO 🎓")
        print("=" * 60)
        print("   [1] 📊 View Predicted Grade Heatmap & Readiness Analytics")
        print("   [2] ⏱️ Launch Daily 15-Minute Micro-Study Routine")
        print("   [3] 🌐 Export HTML Web Studio Dashboard")
        print("   [4] 🚀 Start Live Local Web Server (http://localhost:8080)")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            analytics = analytics_engine.generate_analytics(quiz_manager.progress.module_scores)
            heatmap_str = analytics_engine.render_ascii_heatmap(analytics)
            print("\n" + heatmap_str)
            input("\nPress Enter to continue...")
        elif choice == "2":
            routine = routine_gen.generate_daily_routine()
            print("\n" + "=" * 60)
            print(f" ⏱️ DAILY 15-MINUTE MICRO-STUDY ROUTINE ({routine.date_str})")
            print(" Target: 15 Mins Daily Power Session")
            print("=" * 60)
            for idx, t in enumerate(routine.tasks, 1):
                print(f"\n   Task {idx}: {t.title}")
                print(f"   Details: {t.details}")
            print("=" * 60)
            input("\nPress Enter to return...")
        elif choice == "3":
            analytics = analytics_engine.generate_analytics(quiz_manager.progress.module_scores)
            routine = routine_gen.generate_daily_routine()
            out_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "resources",
                "web_studio.html",
            )
            saved_path = web_studio.export_html_file(analytics, routine, out_file)
            print("\n" + "=" * 60)
            print(" 🌐 WEB STUDIO DASHBOARD HTML EXPORTED SUCCESSFULLY!")
            print(f" File Saved To: {saved_path}")
            print("=" * 60)
            input("\nPress Enter to continue...")
        elif choice == "4":
            analytics = analytics_engine.generate_analytics(quiz_manager.progress.module_scores)
            routine = routine_gen.generate_daily_routine()
            out_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "resources",
                "web_studio.html",
            )
            saved_path = web_studio.export_html_file(analytics, routine, out_file)
            web_studio.start_local_server(saved_path, port=8080)
            input("\nPress Enter to return...")


def run_uk_exam_studio_hub():
    exam_engine = UKExamEngine()
    report_gen = CourseworkReportGenerator()
    socratic_tutor = SocraticTutor()

    while True:
        print("\n" + "=" * 60)
        print(" 📝 MASTER'S EXAM & COURSEWORK REPORT STUDIO 🎓")
        print("=" * 60)
        print("   [1] 📝 Take 2-Hour Timed Exam Simulator (100 Marks)")
        print("   [2] 📄 Generate LaTeX Report Template & Plots")
        print("   [3] 💡 Consult Socratic AI Tutor")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            run_uk_exam_simulator(exam_engine)
        elif choice == "2":
            run_latex_coursework_generator(report_gen)
        elif choice == "3":
            run_socratic_tutor_session(socratic_tutor)


def run_uk_exam_simulator(exam_engine):
    paper = exam_engine.generate_sample_exam_paper()
    print("\n" + "=" * 70)
    print(f" 📝 {paper.title} ({paper.module_code})")
    print(f" ⏳ Time Allowed: {paper.time_limit_minutes} Minutes | Total Marks: {paper.total_marks}")
    print(" Structure: Part A (Conceptual), Part B (Tracing), Part C (Algorithms), Part D (Essay)")
    print("=" * 70)

    user_answers = {}
    question_timings = []

    for q in paper.questions:
        print(f"\n--- {q.section.display_name} | QUESTION {q.question_number} ({q.marks} Marks) ---")
        print(f"Prompt: {q.prompt}")
        if q.code_snippet:
            print(f"\nCode Snippet:\n{q.code_snippet}")

        print("\nWrite your answer below:")
        start_t = QuestionTimer.start_timer()
        ans = sys.stdin.read() if not sys.stdin.isatty() else multiline_input()
        elapsed = QuestionTimer.stop_timer(start_t)

        user_answers[q.id] = ans
        question_timings.append(elapsed)
        print(f"⏱️ Time taken on Question {q.question_number}: {QuestionTimer.format_duration(elapsed)}")

    res = exam_engine.evaluate_exam_submission(paper, user_answers, question_timings)

    print("\n" + "=" * 70)
    print(f" 🎓 EXAMINATION EVALUATION RESULT: {res.uk_classification}")
    print(f"    Total Score: {res.total_score} / {res.max_marks} ({res.percentage:.1f}%)")
    print("-" * 70)
    print(f" ⏱️ PACING ANALYTICS & TIMING:")
    print(f"    Total Exam Duration  : {QuestionTimer.format_duration(res.total_duration_seconds)}")
    print(f"    Avg Time / Question  : {res.avg_seconds_per_question:.1f}s")
    print(f"    Pacing Rating        : {res.pacing_rating}")
    print("=" * 70)
    print(" Section Breakdown:")
    for sec, sc in res.section_breakdown.items():
        print(f"   - {sec}: {sc:.1f} Marks")
    print("-" * 70)
    print(f" 📖 Distinction Feedback Rubric:\n{res.upgrade_feedback}")
    print("=" * 70)
    input("\nPress Enter to continue...")


def run_latex_coursework_generator(report_gen):
    print("\n" + "=" * 60)
    print(" 📄 MASTER'S LATEX COURSEWORK REPORT GENERATOR")
    print("=" * 60)
    title = input("Enter Report Title [default: Autonomous Robotics Evaluation]: ").strip()
    if not title:
        title = "Autonomous Robotics Evaluation"

    template = report_gen.generate_latex_template(title=title)

    print("\n Generated LaTeX Document Preview:\n")
    print("\n".join(template.full_latex_code.split("\n")[:25]))
    print("\n... [Full LaTeX template generated successfully]")

    print("\n Matplotlib Benchmark Plotting Code Snippet:")
    print(report_gen.get_matplotlib_benchmark_code())
    input("\nPress Enter to continue...")


def run_socratic_tutor_session(socratic_tutor):
    print("\n" + "=" * 60)
    print(" 💡 SOCRATIC AI TUTOR")
    print("=" * 60)
    query = input("What concept or code problem are you stuck on?\n> ").strip()
    if query:
        res = socratic_tutor.generate_socratic_guidance(query)
        print("\n" + "=" * 60)
        print(f" {res['non_cs_analogy']}")
        print(f" 💡 HINT: {res['conceptual_hint']}")
        print("\n ❓ SOCRATIC GUIDED QUESTIONS TO DISCOVER THE SOLUTION:")
        for sq in res["socratic_questions"]:
            print(f"   {sq}")
        print("=" * 60)
    input("\nPress Enter to continue...")


def run_ai_robotics_hub():
    math_engine = MathAIEngine()
    pytorch_sandbox = PyTorchSandbox()
    ros2_sandbox = VirtualROS2Sandbox()

    while True:
        print("\n" + "=" * 60)
        print(" 🤖 MSc AI & ROBOTICS SPECIALIZED LEARNING TRACKS")
        print("=" * 60)
        print("   [1] 📐 Math for AI (Linear Algebra, SE(3), Kalman Filters)")
        print("   [2] 🧠 PyTorch Machine Learning & Autograd Graph Sandbox")
        print("   [3] 🤖 Virtual ROS 2 Node Visualizer & Kinematics Simulator")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            run_math_ai_interactive(math_engine)
        elif choice == "2":
            run_pytorch_interactive(pytorch_sandbox)
        elif choice == "3":
            run_ros2_interactive(ros2_sandbox)


def run_math_ai_interactive(math_engine):
    print("\n" + "=" * 60)
    print(" 📐 MATH FOR AI & ROBOTICS - INTERACTIVE SOLVER")
    print("=" * 60)
    print(" Demonstrating 2D SE(2) Homogeneous Transformation Matrix:")
    t_matrix = math_engine.create_2d_transform_matrix(math.radians(45), 3.0, 2.0, "base_link", "camera_link")
    print(f" Frame: {t_matrix.frame_from} -> {t_matrix.frame_to}")
    for row in t_matrix.matrix_data:
        print("   ", row)

    print("\n Demonstrating 1D Kalman Filter State Prediction & Update:")
    res = math_engine.kalman_filter_1d_step(x_estimate=10.0, p_covariance=2.0, measurement=12.5)
    print(f"   Prior Estimate: 10.0 | Measurement: 12.5")
    print(f"   Posterior Estimate: {res['x_estimate']} | Covariance: {res['p_covariance']} | Kalman Gain: {res['kalman_gain']}")
    input("\nPress Enter to continue...")


def run_pytorch_interactive(pytorch_sandbox):
    print("\n" + "=" * 60)
    print(" 🧠 PYTORCH MACHINE LEARNING & AUTOGRAD GRAPH SANDBOX")
    print("=" * 60)
    x = SimulatedTensor([1.5, 2.5], requires_grad=False)
    w = SimulatedTensor([0.5, -1.0], requires_grad=True)
    b = 0.5
    target = 1.0

    res = pytorch_sandbox.autograd_backward(x, w, b, target)
    print(" Simulated PyTorch Autograd Execution:")
    print(f"   Inputs x      : {x.data}")
    print(f"   Weights w     : {w.data}")
    print(f"   Prediction y  : {res['prediction']}")
    print(f"   MSE Loss L    : {res['loss']}")
    print(f"   ∇_w Loss      : {res['grad_w']} (loss.backward())")
    print(f"   ∇_b Loss      : {res['grad_b']}")
    input("\nPress Enter to continue...")


def run_ros2_interactive(ros2_sandbox):
    print("\n" + "=" * 60)
    print(" 🤖 VIRTUAL ROS 2 GRAPH & KINEMATICS SIMULATOR")
    print("=" * 60)
    ros2_sandbox.create_publisher("camera_driver_node", "/image_raw")
    ros2_sandbox.create_publisher("joint_state_broadcaster", "/joint_states")
    ros2_sandbox.create_subscriber("motion_controller_node", "/joint_states")

    ros2_sandbox.publish_message("/joint_states", "sensor_msgs/JointState", {"position": [0.785, 0.523]})
    messages = ros2_sandbox.echo_topic("/joint_states")

    print(" Virtual ROS 2 Active Node Graph:")
    for name, node in ros2_sandbox.nodes.items():
        print(f"   • Node [{name}]")
        print(f"       Publishes  : {node.published_topics}")
        print(f"       Subscribes : {node.subscribed_topics}")

    print("\n Stream: `ros2 topic echo /joint_states`")
    for msg in messages:
        print(f"   [Timestamp {msg.timestamp:.2f}] Topic: {msg.topic_name} | Data: {msg.data}")

    print("\n 2-DOF Robot Arm Forward Kinematics Calculation:")
    fk = ros2_sandbox.forward_kinematics_2dof(l1=1.0, l2=1.0, theta1_rad=math.radians(45), theta2_rad=math.radians(30))
    print(f"   Joint Angles : θ1={fk['joint_angle_1_deg']}°, θ2={fk['joint_angle_2_deg']}°")
    print(f"   End-Effector Position (x, y) : [{fk['end_effector_x']}, {fk['end_effector_y']}]")
    input("\nPress Enter to continue...")


def run_dsa_whiteboard_hub():
    repo = DSARepository()
    evaluator = WhiteboardEvaluator()
    problems = repo.get_all_problems()

    while True:
        print("\n" + "=" * 60)
        print(" 🧩 DATA STRUCTURES & ALGORITHMS (DSA) MASTERY")
        print(" 📝 STEP-BY-STEP WHITEBOARD MODE")
        print("=" * 60)
        print("   [1] 🧩 Browse DSA Problems by Pattern")
        print("   [2] 📝 Launch Interactive 5-Step Whiteboard Mode")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            print("\nAvailable DSA Pattern Problems:")
            for idx, p in enumerate(problems, 1):
                print(f"   [{idx}] {p.title} ({p.pattern.display_name}) [{p.difficulty}]")

            sub_choice = input("\nSelect problem to inspect or [B]ack: ").strip().lower()
            if sub_choice != "b":
                try:
                    idx = int(sub_choice) - 1
                    if 0 <= idx < len(problems):
                        display_dsa_problem(problems[idx])
                except ValueError:
                    print("Invalid selection.")
        elif choice == "2":
            print("\nSelect problem for Whiteboard Mode:")
            for idx, p in enumerate(problems, 1):
                print(f"   [{idx}] {p.title}")

            sub_choice = input("\nSelect problem index: ").strip()
            try:
                idx = int(sub_choice) - 1
                if 0 <= idx < len(problems):
                    run_whiteboard_session(problems[idx], evaluator)
            except ValueError:
                print("Invalid selection.")


def display_dsa_problem(problem):
    print("\n" + "=" * 68)
    print(f" 🧩 PROBLEM: {problem.title}")
    print(f" 📌 PATTERN: {problem.pattern.display_name}")
    print(f" 🎯 DIFFICULTY: {problem.difficulty}")
    print("=" * 68)
    print(f"\n📜 STATEMENT:\n{problem.problem_statement}")
    print(f"\n💡 SAMPLE I/O:\n{problem.sample_input_output}")
    print(f"\n🏛️ INTUITIVE ANALOGY:\n{problem.non_cs_analogy}")
    print(f"\n⚠️ EDGE CASES:\n" + "\n".join(f"  - {e}" for e in problem.edge_cases))
    print(f"\n⚙️ TIME COMPLEXITY:  {problem.time_complexity}")
    print(f"⚙️ SPACE COMPLEXITY: {problem.space_complexity}")
    print(f"\n💻 OPTIMAL CODE SOLUTION:\n{problem.solution_code}")
    print("=" * 68)
    input("\nPress Enter to continue...")


def run_whiteboard_session(problem, evaluator):
    print("\n" + "=" * 70)
    print(" 📝 STEP-BY-STEP WHITEBOARD PRESENTATION")
    print(f" Problem: {problem.title}")
    print(" Candidates MUST document all 5 steps!")
    print("=" * 70)

    print("\n--- STEP 1 of 5: Input / Output Examples ---")
    s1 = input("Write down 2 concrete example cases (inputs -> outputs):\n> ").strip()

    print("\n--- STEP 2 of 5: Key Edge Cases ---")
    s2 = input("List boundary edge cases (e.g. empty inputs, duplicates, single elements):\n> ").strip()

    print("\n--- STEP 3 of 5: Step-by-Step Logic in Plain English ---")
    s3 = input("Explain your algorithmic strategy in plain English:\n> ").strip()

    print("\n--- STEP 4 of 5: Time & Space Complexity Analysis ---")
    s4 = input("Specify expected Big-O Time & Space Complexity (e.g. Time O(N), Space O(1)):\n> ").strip()

    print("\n--- STEP 5 of 5: Python Code Implementation ---")
    print(f"Write your Python solution below for function '{problem.test_cases[0]['function_name'] if problem.test_cases else 'solution'}':")
    s5 = sys.stdin.read() if not sys.stdin.isatty() else multiline_input()

    submission = WhiteboardSubmission(
        problem_id=problem.id,
        step1_examples=s1,
        step2_edge_cases=s2,
        step3_plain_logic=s3,
        step4_complexity=s4,
        step5_code=s5,
    )

    result = evaluator.evaluate_submission(problem, submission)

    print("\n" + "=" * 70)
    print(f" 🎓 WHITEBOARD PRESENTATION RESULT: {result.uk_grade}")
    print("=" * 70)
    print(" 📋 STEP BREAKDOWN:")
    print(f"   [Step 1 - I/O Examples]     : {'✅ PASSED' if result.step_scores['step1_examples'] else '❌ INCOMPLETE'}")
    print(f"   [Step 2 - Edge Cases]       : {'✅ PASSED' if result.step_scores['step2_edge_cases'] else '❌ INCOMPLETE'}")
    print(f"   [Step 3 - Plain Logic]      : {'✅ PASSED' if result.step_scores['step3_plain_logic'] else '❌ INCOMPLETE'}")
    print(f"   [Step 4 - Big-O Complexity] : {'✅ PASSED' if result.step_scores['step4_complexity'] else '❌ INCOMPLETE'}")
    print(f"   [Step 5 - Code Execution]   : {'✅ PASSED' if result.step_scores['step5_code'] else '❌ FAILED'}")
    print("-" * 70)
    print(f" 📖 Evaluation Feedback: {result.feedback}")
    print("=" * 70)
    input("\nPress Enter to return...")


def multiline_input():
    lines = []
    print("(Type your code line by line. Type 'END' on a new line when finished):")
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


def run_python_curriculum_menu():
    curriculum = PythonCurriculum()
    modules = curriculum.get_all_modules()
    engine = PracticeEngine()

    while True:
        print("\n" + "=" * 60)
        print(" 🐍 PYTHON MASTERY - LECTURES & CUMULATIVE Q&A")
        print("=" * 60)
        for mod in modules:
            print(f"   [{mod.order}] {mod.title}")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect a Python module (1-9) or [B]ack: ").strip().lower()
        if choice == "b":
            break
        else:
            try:
                order = int(choice)
                target_mod = next((m for m in modules if m.order == order), None)
                if target_mod:
                    display_lecture_and_run_cumulative_quiz(target_mod, modules, engine)
                else:
                    print("Invalid module number.")
            except ValueError:
                print("Invalid input.")


def display_lecture_and_run_cumulative_quiz(mod, all_modules, engine):
    print("\n" + "=" * 68)
    print(f" 📖 LECTURE PHASE: {mod.title}")
    print("=" * 68)
    print(f"\n📌 SUMMARY:\n{mod.summary}")
    print(f"\n🏛️ INTUITIVE ANALOGY:\n{mod.non_cs_analogy}")
    print(f"\n💻 SYNTAX & EXAMPLES:\n{mod.syntax_guide}")
    print(f"\n⚠️ COMMON TRAPS & GOTCHAS:\n{mod.common_traps}")
    print("=" * 68)
    
    input("\nPress Enter to begin the Cumulative End-of-Module Q&A Session...")
    run_cumulative_quiz_for_module(mod, all_modules, engine)


def run_cumulative_quiz_for_module(mod, all_modules, engine):
    engine.reset_session()
    question_tuples = engine.build_cumulative_question_set(all_modules, mod.order)
    question_timings = []

    print("\n" + "=" * 70)
    print(f" 🧠 CUMULATIVE END-OF-MODULE Q&A SESSION")
    print(f" 📚 Lecture Completed: {mod.title}")
    print(f" 🔁 Testing Scope: Module 1 through Module {mod.order} (Cumulative Recall)")
    print(f" 📊 Total Questions in Quiz: {len(question_tuples)}")
    print("=" * 70)

    for idx, (q, label) in enumerate(question_tuples, 1):
        print(f"\n--- QUESTION {idx} of {len(question_tuples)} [{label}] ---")
        print(f"Prompt: {q.prompt}\n")

        start_t = QuestionTimer.start_timer()
        if q.question_type == QuestionType.MULTIPLE_CHOICE:
            for opt_idx, opt in enumerate(q.options, 1):
                print(f"   [{opt_idx}] {opt}")
            ans = input("\nYour answer (enter number or text): ").strip()
        else:
            if q.analogy_hint:
                print(f"💡 Hint Analogy: {q.analogy_hint}")
            ans = input("\nType your answer: ").strip()

        elapsed = QuestionTimer.stop_timer(start_t)
        question_timings.append(elapsed)

        result = engine.evaluate_answer(q, ans)
        if result.is_correct:
            print(f"\n✅ CORRECT! ({QuestionTimer.format_duration(elapsed)})")
        else:
            print(f"\n❌ INCORRECT ({QuestionTimer.format_duration(elapsed)}). Expected: {result.correct_answer}")

        print(f"📖 Explanation: {result.explanation}")
        if result.distinction_tip:
            print(f"🏆 Distinction Tip: {result.distinction_tip}")

    stats = engine.get_stats()
    total_sec = sum(question_timings)
    avg_sec = total_sec / len(question_tuples) if question_tuples else 0.0
    pacing_rating, _ = QuestionTimer.get_uk_pacing_rating(avg_sec)

    print("\n" + "=" * 70)
    print(f" 🎯 CUMULATIVE QUIZ RESULTS FOR MODULE {mod.order}")
    print(f"    Score: {stats['score']} / {stats['total']} ({stats['percentage']:.1f}%)")
    print("-" * 70)
    print(f" ⏱️ PACING ANALYTICS & TIMING:")
    print(f"    Total Quiz Duration  : {QuestionTimer.format_duration(total_sec)}")
    print(f"    Avg Time / Question  : {avg_sec:.1f}s")
    print(f"    Pacing Rating        : {pacing_rating}")
    print("-" * 70)
    
    if stats["percentage"] >= 70:
        print("    🏆 DEGREE RESULT: DISTINCTION (70%+)")
    elif stats["percentage"] >= 50:
        print("    ✅ DEGREE RESULT: PASS (50%+)")
    else:
        print("    ❌ DEGREE RESULT: FAIL (< 50% - Retake recommended)")
    print("=" * 70)

    input("\nPress Enter to return to curriculum menu...")


def run_dynamic_gated_quizzes_hub():
    curriculum = PythonCurriculum()
    modules = curriculum.get_all_modules()
    generator = DynamicQuizGenerator()
    manager = QuizManager()

    while True:
        print("\n" + "=" * 60)
        print(" 🎯 DYNAMIC GATED QUIZZES & PASS-MARK THRESHOLDS")
        print("=" * 60)
        print("   [1] 🎯 Take Dynamic Module Quiz (Randomized Variations)")
        print("   [2] 🏆 View Unlocked Modules & Distinction Badges")
        print("   [3] 🔄 Retake Quiz with Parameter Mutations")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice in ("1", "3"):
            print("\nAvailable Modules:")
            for mod in modules:
                status = "🔒 Locked"
                if manager.is_module_unlocked(mod.id):
                    score = manager.progress.module_scores.get(mod.id, 0.0)
                    status = f"✅ Unlocked ({score:.0f}%)"
                    if mod.id in manager.progress.distinction_badges:
                        status += " 🏆 Distinction Badge"

                print(f"   [{mod.order}] {mod.title} - {status}")

            sub_choice = input("\nSelect module to quiz: ").strip()
            try:
                mod_num = int(sub_choice)
                target_mod = next((m for m in modules if m.order == mod_num), None)
                if target_mod:
                    if not manager.is_module_unlocked(target_mod.id):
                        print(f"\n🔒 Module {target_mod.order} is locked! You must pass earlier modules (>=50%) to unlock.")
                    else:
                        run_dynamic_quiz_attempt(target_mod.id, generator, manager)
                else:
                    print("Invalid module number.")
            except ValueError:
                print("Invalid selection.")
        elif choice == "2":
            print("\n" + "=" * 60)
            print(" 🏆 USER DEGREE PROGRESS & BADGES")
            print("=" * 60)
            print(" Unlocked Modules:", manager.progress.unlocked_modules)
            print(" Distinction Badges Earned:", manager.progress.distinction_badges)
            print(" Highest Module Scores:")
            for m_id, sc in manager.progress.module_scores.items():
                print(f"   - {m_id}: {sc:.1f}%")
            print("=" * 60)
            input("\nPress Enter to continue...")


def run_dynamic_quiz_attempt(module_id, generator, manager):
    seed = random.randint(1000, 99999)
    questions = generator.generate_quiz_for_module(module_id, seed=seed)
    question_timings = []

    print("\n" + "=" * 70)
    print(f" 🎯 DYNAMIC MODULE QUIZ (Variation Seed: #{seed})")
    print(" Questions test Theory, Output Prediction, Syntax Correction, & Complexity!")
    print("=" * 70)

    user_answers = []
    for idx, q in enumerate(questions, 1):
        print(f"\n--- QUESTION {idx} of {len(questions)} [{q.category.display_name}] ---")
        print(f"Prompt: {q.prompt}")
        if q.code_snippet:
            print(f"\nCode Snippet:\n{q.code_snippet}")

        start_t = QuestionTimer.start_timer()
        if q.options:
            print("")
            for opt_idx, opt in enumerate(q.options, 1):
                print(f"   [{opt_idx}] {opt}")
            ans = input("\nYour answer (enter number or text): ").strip()
        else:
            ans = input("\nType your answer: ").strip()

        elapsed = QuestionTimer.stop_timer(start_t)
        question_timings.append(elapsed)
        user_answers.append(ans)

    res = manager.evaluate_quiz_attempt(module_id, questions, user_answers, question_timings)

    print("\n" + "=" * 70)
    print(f" 🎯 QUIZ EVALUATION RESULT: {res.grade_label}")
    print(f"    Score: {res.score} / {res.total_questions} ({res.percentage:.1f}%)")
    print("-" * 70)
    print(f" ⏱️ PACING ANALYTICS & TIMING:")
    print(f"    Total Quiz Duration  : {QuestionTimer.format_duration(res.total_duration_seconds)}")
    print(f"    Avg Time / Question  : {res.avg_seconds_per_question:.1f}s")
    print(f"    Pacing Rating        : {res.pacing_rating}")
    print("=" * 70)

    input("\nPress Enter to continue...")


def run_srs_flashcards_hub():
    repo = DeckRepository()

    while True:
        due_cards = repo.get_due_cards()
        print("\n" + "=" * 60)
        print(" 🎴 SUPERMEMO SM-2 SPACED REPETITION FLASHCARDS")
        print("=" * 60)
        print(f" 📊 Total Due Cards Today: {len(due_cards)}")
        print("-" * 60)
        print("   [1] 🎴 Start Daily Review Session (Due Cards)")
        print("   [2] 📚 Browse Study Decks (6 Categorized Decks)")
        print("   [3] 📊 View SRS Learning Progress & Card Schedule")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            if not due_cards:
                print("\n🎉 No due cards today! All cards are reviewed.")
                input("\nPress Enter to return...")
            else:
                run_srs_review_session(due_cards, repo)
        elif choice == "2":
            browse_study_decks(repo)
        elif choice == "3":
            view_srs_stats(repo)


def run_srs_review_session(cards, repo):
    print(f"\n🚀 STARTING SRS REVIEW SESSION ({len(cards)} cards)")
    print("-" * 60)

    for idx, card in enumerate(cards, 1):
        print(f"\n" + "=" * 60)
        print(f" 🎴 CARD {idx} of {len(cards)} [{card.deck_id}]")
        print(f" 📌 FRONT: {card.front}")
        if card.non_cs_analogy:
            print(f" 🏛️ ANALOGY: {card.non_cs_analogy}")
        print("=" * 60)

        input("\nPress Enter to reveal answer...")
        print(f"\n 💡 BACK / ANSWER:\n {card.back}")
        print("=" * 60)

        print("\n Rate your recall confidence (SuperMemo SM-2):")
        print("   [0] Complete Blackout (Forgot completely)")
        print("   [1] Incorrect Answer")
        print("   [2] Hesitant / Hard")
        print("   [3] Good (Correct with effort)")
        print("   [4] Easy (Correct with slight hesitation)")
        print("   [5] Perfect Recall")

        rating_input = input("\nEnter rating (0-5): ").strip()
        try:
            rating = int(rating_input)
            if 0 <= rating <= 5:
                repo.sm2.process_review(card, rating)
                repo.save_state()
                print(f" ✅ Card updated! Next review in {card.interval_days} day(s) (EF={card.ease_factor:.2f}).")
            else:
                print("Invalid rating. Defaulting to 3 (Good).")
                repo.sm2.process_review(card, 3)
                repo.save_state()
        except ValueError:
            print("Invalid rating. Defaulting to 3 (Good).")
            repo.sm2.process_review(card, 3)
            repo.save_state()

    print("\n🎉 DAILY SRS REVIEW SESSION COMPLETE!")
    input("\nPress Enter to return...")


def browse_study_decks(repo):
    decks = repo.get_all_decks()
    print("\n" + "=" * 60)
    print(" 📚 CATEGORIZED STUDY DECKS")
    print("=" * 60)
    for idx, deck in enumerate(decks, 1):
        print(f"\n [{idx}] {deck.name}")
        print(f"     Description: {deck.description}")
        print(f"     Total Cards: {len(deck.cards)}")

    sub_choice = input("\nSelect deck index to view cards or [B]ack: ").strip().lower()
    if sub_choice == "b":
        return
    else:
        try:
            idx = int(sub_choice) - 1
            if 0 <= idx < len(decks):
                target_deck = decks[idx]
                print(f"\n--- CARDS IN {target_deck.name} ---")
                for c in target_deck.cards:
                    print(f"\n  • Front: {c.front}")
                    print(f"    Back:  {c.back}")
                    print(f"    Interval: {c.interval_days}d | EF: {c.ease_factor:.2f} | Reps: {c.repetitions}")
                input("\nPress Enter to continue...")
        except ValueError:
            print("Invalid selection.")


def view_srs_stats(repo):
    decks = repo.get_all_decks()
    total_cards = sum(len(d.cards) for d in decks)
    due_cards = repo.get_due_cards()

    print("\n" + "=" * 60)
    print(" 📊 SPACED REPETITION SYSTEM (SRS) STATISTICS")
    print("=" * 60)
    print(f" Total Study Decks: {len(decks)}")
    print(f" Total Flashcards:  {total_cards}")
    print(f" Due Cards Today:   {len(due_cards)}")
    print("=" * 60)
    input("\nPress Enter to return...")


def run_syntax_drills_hub():
    bank = DrillBank()
    anti_copilot = AntiCopilotEngine()
    exam_mode = NoCompilerExamMode()

    while True:
        print("\n" + "=" * 60)
        print(" ⚡ ACTIVE SYNTAX MEMORY & ANTI-COPILOT DRILLS")
        print("=" * 60)
        print("   [1] ⚡ Anti-Copilot Raw Typing Drills (Muscle Memory)")
        print("   [2] 📝 Paper-and-Pen / No-Compiler Written Exam Mode")
        print("   [3] 🧩 Fill-in-the-Blank Code Completion")
        print("   [4] 🔍 Code Tracing & Output Prediction")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect drill option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "1":
            drills = bank.get_drills_by_type(DrillType.ANTI_COPILOT_TYPING)
            for d in drills:
                print("\n" + "=" * 60)
                print(f" 🎯 DRILL: {d.title}")
                print(f" ℹ️  {d.description}")
                print("=" * 60)
                print("\nTarget Syntax to Type From Memory:\n")
                print(d.target_syntax)
                print("\n" + "-" * 60)
                print("Type out the exact syntax below (NO AUTOCOMPLETE ALLOWED!):")
                user_typed = sys.stdin.read() if not sys.stdin.isatty() else multiline_input()

                res = anti_copilot.evaluate_typing_drill(d, user_typed)
                print("\n" + "=" * 60)
                print(f" 📊 DRILL EVALUATION: {res.uk_grade}")
                print("=" * 60)
                if res.is_perfect:
                    print(" ✅ PERFECT MEMORY RECALL!")
                else:
                    print(" 🔍 LINE-BY-LINE DIFF FEEDBACK:\n")
                    print(res.diff_feedback)
                    if not res.ast_valid:
                        print(f"\n ❌ AST Syntax Error: {res.error_message}")
                print("=" * 60)
                input("\nPress Enter to continue...")
        elif choice == "2":
            drills = bank.get_drills_by_type(DrillType.NO_COMPILER_EXAM)
            for d in drills:
                print("\n" + "=" * 60)
                print(f" 📝 WRITTEN EXAM PAPER: {d.title}")
                print(f" 📜 Problem Description:\n{d.description}")
                print("=" * 60)
                print("\nWrite your full Python code solution below (NO IDE SQUIGGLES / NO HELPERS):")
                user_code = sys.stdin.read() if not sys.stdin.isatty() else multiline_input()

                res = exam_mode.evaluate_written_exam(d, user_code)
                print("\n" + "=" * 60)
                print(f" 🎓 EXAM EVALUATION RESULT: {res.uk_grade}")
                print("=" * 60)
                print(f" Feedback: {res.diff_feedback}")
                print("=" * 60)
                input("\nPress Enter to continue...")
        elif choice == "3":
            drills = bank.get_drills_by_type(DrillType.FILL_IN_BLANK)
            for d in drills:
                print("\n--- FILL IN THE BLANK ---")
                print(d.description)
                print(f"\nCode Snippet:\n{d.template_code}")
                ans = input("\nType missing keyword/syntax: ").strip()
                if ans.strip().lower() == d.target_syntax.strip().lower():
                    print("✅ CORRECT!")
                else:
                    print(f"❌ Expected: {d.target_syntax}")
                print(f"Explanation: {d.explanation}")
            input("\nPress Enter to continue...")
        elif choice == "4":
            drills = bank.get_drills_by_type(DrillType.CODE_TRACING)
            for d in drills:
                print("\n--- CODE TRACING & OUTPUT PREDICTION ---")
                print(d.description)
                print(f"\nCode Snippet:\n{d.template_code}")
                ans = input("\nPredict the printed output: ").strip()
                if ans.strip() == d.expected_output.strip():
                    print("✅ CORRECT PREDICTION!")
                else:
                    print(f"❌ Expected output: {d.expected_output}")
                print(f"Explanation: {d.explanation}")
            input("\nPress Enter to continue...")


def run_multi_format_doc_ingestion():
    os.makedirs(USER_UPLOADS_DIR, exist_ok=True)
    downloader = DocDownloader()
    parser = MultiFormatParser()
    auto_gen = AutoCurriculumGenerator()
    downloader.download_all()

    while True:
        print("\n" + "=" * 60)
        print(" 📄 MULTI-FORMAT DOCUMENT INGESTION ENGINE (RAG)")
        print("=" * 60)
        print(" Upload directory:", USER_UPLOADS_DIR)
        print("-" * 60)

        uploaded_files = os.listdir(USER_UPLOADS_DIR) if os.path.exists(USER_UPLOADS_DIR) else []
        if uploaded_files:
            for idx, f in enumerate(uploaded_files, 1):
                print(f"   [{idx}] {f}")
        else:
            print("   (No files currently in user_uploads/ folder)")

        print("\n Options:")
        print("   [P] Parse Python official docs")
        print("   [F] Enter custom local file path")
        print("   [B] Back to Main Menu")

        choice = input("\nSelect option: ").strip().lower()
        if choice == "b":
            break
        elif choice == "p":
            python_docs_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "resources", "python_docs"
            )
            files = [f for f in os.listdir(python_docs_dir) if f.endswith(".html")]
            for idx, f in enumerate(files, 1):
                print(f"   [{idx}] {f}")
            sub_choice = input("\nSelect document index: ").strip()
            try:
                sub_idx = int(sub_choice) - 1
                if 0 <= sub_idx < len(files):
                    file_path = os.path.join(python_docs_dir, files[sub_idx])
                    doc_data = parser.parse_file(file_path)
                    mod = auto_gen.generate_module_from_doc(doc_data)
                    print(f"\nGenerated 5-tier module for {mod.title}")
                    input("\nPress Enter to continue...")
            except ValueError:
                print("Invalid selection.")


def run_foundation_hub():
    engine = AnalogyEngine()
    stone = MathRosettaStone()
    print("\n" + "=" * 60)
    print(" 🌉 FOUNDATION & MATH ROSETTA STONE")
    print("=" * 60)
    for c in engine.get_all():
        print(f"   - {c.concept} ({c.non_cs_domain})")
    print("\nGreek Symbols Available:", list(stone.get_greek_alphabet().keys()))
    input("\nPress Enter to return...")


def main():
    print_banner()
    while True:
        print("\n Main Menu Options:")
        print("   [1] 💻 Grade Analytics Dashboard, Daily Routine & Web Studio")
        print("   [2] 🐍 Learn Python Lectures & Cumulative Q&A (M1 -> MN)")
        print("   [3] 📝 Exam Simulator & LaTeX Coursework Studio 🎓")
        print("   [4] 🤖 MSc AI & Robotics Tracks (Virtual ROS 2 & PyTorch)")
        print("   [5] 🧩 DSA Pattern Tracks & 5-Step Whiteboard Mode")
        print("   [6] 🎯 Dynamic Gated Quizzes & Pass Thresholds (Retake Mutations)")
        print("   [7] ⚡ Active Syntax Memory & Anti-Copilot Drills (No-Compiler Exam)")
        print("   [8] 🎴 Flashcards & Spaced Repetition (SuperMemo SM-2 SRS)")
        print("   [9] 📄 Multi-Format Doc Ingestor (PDF, MD, HTML, Text)")
        print("   [10] 🌉 Intuitive Analogy & Rosetta Stone Engine")
        print("   [K] 🔑 Configure Gemini AI API Key")
        print("   [Q] Quit Application")
        print("-" * 72)

        choice = input("Enter choice (1-10, K or Q): ").strip().lower()
        if choice == "1":
            run_analytics_studio_hub()
        elif choice == "2":
            run_python_curriculum_menu()
        elif choice == "3":
            run_uk_exam_studio_hub()
        elif choice == "4":
            run_ai_robotics_hub()
        elif choice == "5":
            run_dsa_whiteboard_hub()
        elif choice == "6":
            run_dynamic_gated_quizzes_hub()
        elif choice == "7":
            run_syntax_drills_hub()
        elif choice == "8":
            run_srs_flashcards_hub()
        elif choice == "9":
            run_multi_format_doc_ingestion()
        elif choice == "10":
            run_foundation_hub()
        elif choice == "k":
            configure_gemini_api_key()
        elif choice in ("q", "quit", "exit", "0"):
            print("\nGoodbye! Keep building cumulative mastery for your Master's Distinction! 🎓\n")
            break
        else:
            print("\nInvalid choice. Please select 1-10, K or Q.")


if __name__ == "__main__":
    main()
