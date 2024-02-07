"""
This script provides a minimal example showing how tu run multiple Kratos simulations in parallel, exploiting concurrency capabilities of modern high performance computing systems.
The main operations we do are
* Create an analysis stage, here called SimulationScenario, which is derived from the analysis stage of our problem, in this case analysis stage.
* Serialize the Kratos project parameters and the Kratos model within a task.
* Run the Kratos simulation in parallel within a task.
The script works correctly under the following scenarios:
* workflow is serial,
* workflow is serial and managed by distributed environment scheduler PyCOMPSs.
To run the first scenario:
python3 launch-multiple-simulations-pycompss.py
To run with runcompss the second scenario:
sh run.sh
In this last case, the environment variable EXAQUTE_BACKEND has to be changed to pycompss; see the documentation related to the configuration of COMPSs for details.

Dependencies
------------
- KratosMultiphysics ≥ 9.0."Dev"-96fb824069, and applications:
   - ConvectionDiffusionApplication,
- COMPSs ≥ 2.8 (to run in parallel).
"""

# Import Python libraries
import numpy as np
import pickle

# Importing the Kratos Library
import KratosMultiphysics
import KratosMultiphysics.ConvectionDiffusionApplication
from KratosMultiphysics.analysis_stage import AnalysisStage

# Import PyCOMPSs
from exaqute import task, FILE_IN, get_value_from_remote
from exaqute import init as exaqute_init
exaqute_init() # must not be called more than once



def GetValueFromListList(values,iteration):
    """
    Function generating the random sample; in this case, we return a value from an input
    """
    value = values[iteration]
    return value


@task(returns=1)
def ExecuteInstance_Task(pickled_model,pickled_parameters,heat_flux_list,instance):
    """
    Function executing an instance of the problem
    input:
            pickled_model:      serialization of the model
            pickled_parameters: serialization of the Project Parameters
            heat_flux_list:     list of values for \varepsilon
            instance:           iteration number
    output:
            QoI: Quantity of Interest
    """
    # overwrite the old model serializer with the unpickled one
    model_serializer = pickle.loads(pickled_model)
    current_model = KratosMultiphysics.Model()
    model_serializer.Load("ModelSerialization",current_model)
    del(model_serializer)
    # overwrite the old parameters serializer with the unpickled one
    serialized_parameters = pickle.loads(pickled_parameters)
    current_parameters = KratosMultiphysics.Parameters()
    serialized_parameters.Load("ParametersSerialization",current_parameters)
    del(serialized_parameters)
    # get sample
    sample = GetValueFromListList(heat_flux_list,instance)
    simulation = SimulationScenario(current_model,current_parameters,sample)
    simulation.Run()
    QoI = simulation.EvaluateQuantityOfInterest()
    return QoI


@task(parameter_file_name=FILE_IN,returns=2)
def SerializeModelParameters_Task(parameter_file_name):
    """
    Function serializing and pickling the model and the parameters of the problem
    input:
            parameter_file_name: path of the Project Parameters file
    output:
            pickled_model:      model serializaton
            pickled_parameters: project parameters serialization
    """
    with open(parameter_file_name,'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())
    model = KratosMultiphysics.Model()
    # parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(model_part_file_name[:-5])
    fake_sample = 0.25
    simulation = SimulationScenario(model,parameters,fake_sample)
    simulation.Initialize()
    # reset general flags
    # it is not required to remove the materials, since the Kratos variable
    # IS_RESTARTED is set to True
    simulation.model.GetModelPart(parameters["solver_settings"]["model_part_name"].GetString()).ProcessInfo.SetValue(KratosMultiphysics.IS_RESTARTED,True)
    # serialize
    serialized_model = KratosMultiphysics.StreamSerializer()
    serialized_model.Save("ModelSerialization",simulation.model)
    serialized_parameters = KratosMultiphysics.StreamSerializer()
    serialized_parameters.Save("ParametersSerialization",simulation.project_parameters)
    # pickle dataserialized_data
    pickled_model = pickle.dumps(serialized_model, 2) # second argument is the protocol and is NECESSARY (according to pybind11 docs)
    pickled_parameters = pickle.dumps(serialized_parameters, 2)
    KratosMultiphysics.Logger.PrintInfo("SerializeModelParameters_Task", "Model and parameters serialized correctly.")
    return pickled_model,pickled_parameters

class SimulationScenario(AnalysisStage):
    """
    This SimulationScenario analysis stage class solves the elliptic PDE in (0,1)^2 with zero Dirichlet boundary conditions
    -lapl(u) = xi*f
    f= -432*(x**2+y**2-x-y)
    and computes the Quantity of Interest
    Q = int_(0,1)^2 u(x,y)dxdy
    where psi is the random variable and follows a beta distribution Beta(2,6)
    """
    def __init__(self,input_model,input_parameters,sample):
        self.sample = sample
        super(SimulationScenario,self).__init__(input_model,input_parameters)
        self._GetSolver().main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NODAL_AREA)

    def _CreateSolver(self):
        import KratosMultiphysics.ConvectionDiffusionApplication.convection_diffusion_stationary_solver
        return KratosMultiphysics.ConvectionDiffusionApplication.convection_diffusion_stationary_solver.CreateSolver(self.model,self.project_parameters["solver_settings"])

    def ModifyInitialProperties(self):
        """
        Method introducing the stochasticity in the right hand side defining the forcing function and apply the stochastic contribute
        """
        model_part_name = self.project_parameters["problem_data"]["model_part_name"].GetString()
        for node in self.model.GetModelPart(model_part_name).Nodes:
            coord_x = node.X
            coord_y = node.Y
            forcing = -432.0 * (coord_x**2 + coord_y**2 - coord_x - coord_y)
            node.SetSolutionStepValue(KratosMultiphysics.HEAT_FLUX,forcing*self.sample)

    def EvaluateQuantityOfInterest(self):
        """
        Method evaluating the QoI of the problem: int_{domain} TEMPERATURE(x,y) dx dy
        """
        KratosMultiphysics.CalculateNodalAreaProcess(self._GetSolver().main_model_part,2).Execute()
        Q = 0.0
        for node in self._GetSolver().main_model_part.Nodes:
            Q = Q + (node.GetSolutionStepValue(KratosMultiphysics.NODAL_AREA)*node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE))
        return Q


if __name__ == '__main__':

    # set the ProjectParameters.json path
    parameter_file_name = "problem_settings/project_parameters.json"
    # create a serialization of the model and of the project parameters
    pickled_model,pickled_parameters = SerializeModelParameters_Task(parameter_file_name)
    # set batch size and initialize qoi list where to append Quantity of Interests values
    batch_size = 20
    qoi = []
    # define the list for heat flux values
    heat_flux_list = np.random.beta(2.0,6.0,batch_size)
    # start algorithm
    for instance in range (0,batch_size):
        qoi.append(ExecuteInstance_Task(pickled_model,pickled_parameters,heat_flux_list,instance))

    # synchronize to local machine
    qoi = get_value_from_remote(qoi)
    print("\nqoi values:\n",qoi)
