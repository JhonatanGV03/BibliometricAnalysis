
from collections import Counter

palabras_clave= {
    "Habilidades" : ["Abstraction", "Algorithm", "Algorithmic_thinking", "Coding", "Collaboration", "Cooperation", "Creativity", "Critical_thinking", "Debug", "Decomposition", "Evaluation", "Generalization", "Logic", "Logical_thinking", "Modularity", "Patterns_recognition", "Problem_solving", "Programming"],
    "Conceptos Computacionales" : ["Conditionals", "Control_structures", "Directions", "Events", "Funtions", "Loops", "Modular_structure", "Parallelism", "Sequences", "Software", "hardware", "Variables"],
    "Actitudes" : ["Emotional", "Engagement", "Motivation", "Perceptions", "Persistence", "Self-efficacy", "Self-perceived"],
    "Propiedades psicometricas" : ["Classical_Test_Theory","CTT","Confirmatory_Factory_Analysis", "CFA", "Exploratory_Factor_Analysis", "EFA", "Item_Response_Theory", "IRT", "Reliability", "Structural_Equation_Model", "SEM", "Validity"],
    "Herramienta de evaluación" : ["Beginners_Computational_Thinking_test", "BCTt", "Coding_Attitudes_Survey", "ESCAS", "Collaborative_Computing_Observation_Instrument", "Competent_Computational_Thinking_test", "cCTt", "Computational_thinking_skills_test", "CTST", "Computational_concepts", "Computational_thinking_Assessment_for_Chinese_Elementary_Students", "CTA", "CES", "Computational_Thinking_Challenge", "CTC", "Computational_Thinking_Levels_Scale", "CTLS", "Computational_Thinking_Scale", "CTS", "Computational_Thinking_Skill_Levels_Scale", "Computational_Thinking_Test", "CTt", "Computational_Thinking_Test_for_Elementary_School_Students", "Computational_Thinking_Test_for_Lower_Primary", "CTtLP", "Computational_thinking-skill_tasks_on_numbers_and_arithmetic", "Computerized_Adaptive_Programming_Concepts_Test", "CAPCT", "CT_Scale", "CTS", "Elementary_Student_Coding_Attitudes_Survey", "ESCAS", "General_Self-efficacy_scale", "ICT_competency_test", "Instrument_of_computational_identity", "KBIT_fluid_intelligence_subtest", "Mastery_of_computational_concepts_Test_and_an_Algorithmic_Test", "Multidimensional_21st_Century_Skills_Scale", "Self-efficacy_scale", "STEM_learning_attitude_scale", "The_computational_thinking_scale"],
    "Diseño de investigación" : ["No_experimental", "Experimental", "Longitudinal_research", "Mixed_methods", "Post-test", "Pre-test", "Quasi-experiments"],
    "Nivel de escolaridad" : ["Upper_elementary_education - Upper_elementary_school", "Primary_school - Primary_education - Elementary_school", "Early_childhood_education – Kindergarten-Preschool", "Secondary_school - Secondary_education", "high_school - higher_education", "University – College"],
    "Medio" :["Block_programming","Mobile_application","Pair_programming","Plugged_activities","Programming","Robotics","Spreadsheet","STEM","Unplugged_activities"],
    "Estrategia" : ["Construct-by-self_mind_mapping","Construct-on-scaffold_mind_mapping","Design-based_learning","Evidence-centred_design_approach","Gamification","Reverse_engineering_pedagogy","Technology-enhanced_learning","Collaborative_learning","Cooperative_learning","Flipped_classroom","Game-based_learning","Inquiry-based_learning","Personalized_learning","Problem-based_learning","Project-based_learning","Universal_design_for_learning"],
    "Herramienta" : ["Alice", "Arduino","Scratch","ScratchJr", "Blockly Games","Code.org","Codecombat","CSUnplugged","Robot Turtles","Hello Ruby","Kodable","LightbotJr","KIBO robots","BEE BOT","CUBETTO","Minecraft","Agent Sheets","Mimo","Py– Learn","SpaceChem"]
}

# Leer los tokens guardados
with open("tokens.txt", "r", encoding="utf-8") as f:
    todos_los_tokens = f.read().splitlines()

conteo_tokens = Counter(todos_los_tokens)

coincidencias = []

# Recorrer por categoría y palabras
for categoria, lista_palabras in palabras_clave.items():
    for palabra in lista_palabras:
        cantidad = conteo_tokens.get(palabra, 0)
        if cantidad > 0:
            coincidencias.append((palabra, cantidad, categoria))

# Ejemplo de impresión
for palabra, cantidad, categoria in coincidencias:
    print(f"{palabra}: {cantidad} apariciones (Categoría: {categoria})")
