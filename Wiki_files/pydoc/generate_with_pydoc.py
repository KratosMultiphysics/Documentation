import pydoc
import html2text
import KratosMultiphysics
import pkgutil
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

package=KratosMultiphysics
list_modules = []
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+".",
                                                      onerror=lambda x: None):
    list_modules.append(modname)

import sys

file_geometries = open("Geometry" + ".md","w")
geometries_string = "# List of geometries accesible via python\n"

file_linear_solvers = open("LinearSolvers" + ".md","w")
linear_solvers_string = "# List of linear solvers accesible via python\n"

direct_solvers_string = "\n## Direct solvers: \n"
iterative_solvers_string = "\n## Iterative solvers: \n"
complex_solvers_string = "\n## Complex solvers: \n"
preconditioner_string = "\n## Preconditioners: \n"

file_strategies = open("Strategies" + ".md","w")
strategies_string = "# List of strategies accesible via python\n"

solving_strategies_string = "\n## Solving strategies: \n"
conv_criteria_string = "\n## Convergence criteria: \n"
scheme_string = "\n## Schemes: \n"
builder_and_solvers_string = "\n## Building and solvers: \n"

file_utilities = open("Utilities" + ".md","w")
utilities_string = "# List of utilities accesible via python\n"

file_processes = open("Processes" + ".md","w")
processes_string = "# List of processes accesible via python\n"

file_containers = open("Containers" + ".md","w")
containers_string = "# List of containers accesible via python\n"

kernel_containers_string = "\n## Kernel containers: \n"
mesh_containers_string = "\n## Mesh containers: \n"
algebra_containers_string = "\n## Algebra containers containers: \n"
other_containers_string = "\n## Others containers: \n"

file_io = open("IO" + ".md","w")
io_string = "# List of IO classes accesible via python\n"

file_others = open("Others" + ".md","w")
others_string = "# List of others accesible via python\n"

file_flags = open("Flags" + ".md","w")
variables_string = "# List of variables accesible via python\n"

file_variables = open("Variables" + ".md","w")
flags_string = "# List of flags accesible via python\n"

StringVariable_string = "\n## String variables: \n"
BoolVariable_string = "\n## Bool variables: \n"
IntegerVariable_string = "\n## Integer variables: \n"
IntegerVectorVariable_string = "\n## Integer variables variables: \n"
DoubleVariable_string = "\n## Double variables: \n"
VectorVariable_string = "\n## Vector variables: \n"
Array1DVariable3_string = "\n## Array(3) variables: \n"
Array1DVariable6_string = "\n## Array(6) variables: \n"
VectorComponentVariable_string = "\n## Vector (component) variables: \n"
Array1DComponentVariable_string = "\n## Array (component) variables: \n"
MatrixVariable_string = "\n## Matrix variables: \n"
ConstitutuveLawVariable_string = "\n## Constitutive law variables: \n"
ConvectionDiffusionSettingsVariable_string = "\n## ConvectionDiffusionSettingsVariable variables: \n"
RadiationSettingsVariable_string = "\n## Radiation settings variables: \n"
DoubleQuaternionVariable_string = "\n## Quaternion variables: \n"

for name in dir(package):
    if not  "__" in name:
        exec_string = "my_type = type(KratosMultiphysics"+"."+name+")"
        exec(exec_string)
        my_type_string = str(my_type)
        name_class = "KratosMultiphysics"+"."+name
        pydoc.writedoc(name_class)
        html_text = open(name_class + ".html", "r").read()
        md_text = html2text.html2text(html_text)
        md_text = md_text.replace("Kratos.html#","KratosMultiphysics.")
        if ("Variable" in my_type_string):
            directory_name = "Variables/"
            ensure_dir(directory_name)
            if ("StringVariable" in my_type_string):
                StringVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("BoolVariable" in my_type_string):
                BoolVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("IntegerVariable" in my_type_string):
                IntegerVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("IntegerVectorVariable" in my_type_string):
                IntegerVectorVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("DoubleVariable" in my_type_string):
                DoubleVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("VectorVariable" in my_type_string):
                VectorVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Array1DVariable3" in my_type_string):
                Array1DVariable3_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Array1DVariable6" in my_type_string):
                Array1DVariable6_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("VectorComponentVariable" in my_type_string):
                VectorComponentVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Array1DComponentVariable" in my_type_string):
                Array1DComponentVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("MatrixVariable" in my_type_string):
                MatrixVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("ConstitutuveLawVariable" in my_type_string):
                ConstitutuveLawVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("ConvectionDiffusionSettingsVariable" in my_type_string):
                ConvectionDiffusionSettingsVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("RadiationSettingsVariable" in my_type_string):
                RadiationSettingsVariable_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("DoubleQuaternionVariable" in my_type_string):
                DoubleQuaternionVariable_string += "* [**" + name + "**](" + name_class + ")\n"
        elif ("Kratos.Flags" in my_type_string):
            directory_name = "Flags/"
            ensure_dir(directory_name)
            flags_string += "* [**" + name + "**]("  + name_class + ")\n"
        elif (name == "kratos_globals"):
            directory_name = "Classes/"
            ensure_dir(directory_name)
        elif (not "module" in my_type_string):
            directory_name = "Classes/"
            ensure_dir(directory_name)
            if ("Methods inherited from [Process]" in md_text or name == "Process"):
                processes_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [Geometry]" in md_text or name == "Geometry"):
                geometries_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [DirectSolver]" in md_text or name == "DirectSolver"):
                direct_solvers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [IterativeSolver]" in md_text or name == "IterativeSolver"):
                iterative_solvers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [Preconditioner]" in md_text or name == "Preconditioner"):
                preconditioner_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [ComplexLinearSolver]" in md_text or name == "ComplexLinearSolver" ):
                complex_solvers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [LinearSolver]" in md_text or name == "LinearSolver"):
                linear_solvers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [SolvingStrategy]" in md_text or "Methods inherited from [ResidualBasedNewtonRaphsonStrategy]" in md_text or name == "SolvingStrategy"):
                solving_strategies_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [Scheme]" in md_text or name == "Scheme"):
                scheme_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [BuilderAndSolver]" in md_text or name == "BuilderAndSolver"):
                builder_and_solvers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [ConvergenceCriteria]" in md_text or name == "ConvergenceCriteria"):
                conv_criteria_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Methods inherited from [IO]" in md_text or name == "IO"):
                io_string += "* [**" + name + "**](" + name_class + ")\n"
            elif ("Utility" in name or "Utilities" in name or "Utils" in name):
                utilities_string += "* [**" + name + "**](" + name_class + ")\n"
            elif (name == "Tester" or name == "Kernel" or name == "Communicator" or name == "Flags" or name == "VariableData"):
                kernel_containers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif (name == "Vector" or name == "Matrix"):
                algebra_containers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif (name == "Model" or name == "ModelPart" or name == "Point" or name == "Dof" or name == "Condition" or name == "Element" or name == "Properties" or name == "Node" or name == "Buffer" or name == "Mesh" or name == "ProcessInfo"):
                mesh_containers_string += "* [**" + name + "**](" + name_class + ")\n"
            elif (name == "PiecewiseLinearTable" or name == "ConstitutiveLaw"  or name == "Parameters" or name == "Logger"):
                other_containers_string += "* [**" + name + "**](" + name_class + ")\n"
            else:
                others_string += "* [**" + name + "**](" + name_class + ")\n"
        else:
            continue
        file_class = open(directory_name+name_class + ".md","w")
        file_class.write(md_text)
        file_class.close()

variables_string += StringVariable_string+BoolVariable_string+IntegerVariable_string+IntegerVectorVariable_string+DoubleVariable_string+VectorVariable_string+Array1DVariable3_string+Array1DVariable6_string+VectorComponentVariable_string+Array1DComponentVariable_string+MatrixVariable_string+ConstitutuveLawVariable_string+ConvectionDiffusionSettingsVariable_string+RadiationSettingsVariable_string+DoubleQuaternionVariable_string
file_variables.write(variables_string)
file_variables.close()
file_flags.write(flags_string)
file_flags.close()

file_geometries.write(geometries_string)
file_geometries.close()

linear_solvers_string += direct_solvers_string + iterative_solvers_string + complex_solvers_string + preconditioner_string
file_linear_solvers.write(linear_solvers_string)
file_linear_solvers.close()

strategies_string += scheme_string + conv_criteria_string + builder_and_solvers_string + solving_strategies_string
file_strategies.write(strategies_string)
file_strategies.close()

file_utilities.write(utilities_string)
file_utilities.close()

file_processes.write(processes_string)
file_processes.close()

containers_string += kernel_containers_string + mesh_containers_string + algebra_containers_string + other_containers_string
file_containers.write(containers_string)
file_containers.close()

file_io.write(io_string)
file_io.close()

file_others.write(others_string)
file_others.close()

dir_name = os.getcwd()
dir_list = os.listdir(dir_name)

for item in dir_list:
    if item.endswith(".html"):
        os.remove(os.path.join(dir_name, item))
