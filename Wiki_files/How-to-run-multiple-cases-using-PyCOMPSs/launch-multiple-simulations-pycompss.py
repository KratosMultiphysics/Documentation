from __future__ import absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7

# Importing the Kratos Library
import KratosMultiphysics

# Import applications
import KratosMultiphysics.ConvectionDiffusionApplication as KratosConvDiff

# Importing the base class
from analysis_stage import AnalysisStage

# Import packages
import numpy as np

# Import cpickle to pickle the serializer
try:
    import cpickle as pickle  # Use cPickle on Python 2.7
except ImportError:
    import pickle

# Import pycompss
from pycompss.api.task import task
from pycompss.api.api import compss_wait_on
from pycompss.api.parameter import *


"""
This SimulationScenario analysis stage class solves the elliptic PDE in (0,1)^2 with zero Dirichlet boundary conditions
-lapl(u) = xi*f
f= -432*(x**2+y**2-x-y)
and computes the Quantity of Interest (QoI)
Q = int_(0,1)^2 u(x,y)dxdy
where psi is the random variable and follows a beta distribution Beta(2,6)
"""
class SimulationScenario(AnalysisStage):
    def __init__(self,input_model,input_parameters,sample):
        self.sample = sample
        super(SimulationScenario,self).__init__(input_model,input_parameters)
        self._GetSolver().main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NODAL_AREA)

    def _CreateSolver(self):
        import convection_diffusion_stationary_solver
        return convection_diffusion_stationary_solver.CreateSolver(self.model,self.project_parameters["solver_settings"])

    # function indtroducing the stochasticity in the right hand side defining the forcing function and apply the stochastic contribute
    def ModifyInitialProperties(self):
        model_part_name = self.project_parameters["problem_data"]["model_part_name"].GetString()
        for node in self.model.GetModelPart(model_part_name).Nodes:
            coord_x = node.X
            coord_y = node.Y
            forcing = -432.0 * (coord_x**2 + coord_y**2 - coord_x - coord_y)
            node.SetSolutionStepValue(KratosMultiphysics.HEAT_FLUX,forcing*self.sample)

    # function evaluating the QoI of the problem: int_{domain} TEMPERATURE(x,y) dx dy
    def EvaluateQuantityOfInterest(self):
        KratosMultiphysics.CalculateNodalAreaProcess(self._GetSolver().main_model_part,2).Execute()
        Q = 0.0
        for node in self._GetSolver().main_model_part.Nodes:
            Q = Q + (node.GetSolutionStepValue(KratosMultiphysics.NODAL_AREA)*node.GetSolutionStepValue(KratosMultiphysics.TEMPERATURE))
        return Q


###############################################################################################################################################################################


# function generating the random sample
def GetValueFromListList(values,iteration):
    value = values[iteration]
    return value


"""
function executing an instance of the problem
input:
        pickled_model:      serialization of the model
        pickled_parameters: serialization of the Project Parameters
        heat_flux_list:     list of values for \varepsilon
        instance:           iteration number
output:
        QoI: Quantity of Interest
"""
@task(returns=1)
def ExecuteInstance_Task(pickled_model,pickled_parameters,heat_flux_list,instance):
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
    sample = GetValueFromListList(heat_flux_list,instance) # take
    simulation = SimulationScenario(current_model,current_parameters,sample)
    simulation.Run()
    QoI = simulation.EvaluateQuantityOfInterest()
    return QoI


"""
function serializing and pickling the model and the parameters of the problem
input:
        parameter_file_name: path of the Project Parameters file
output:
        pickled_model:      model serializaton
        pickled_parameters: project parameters serialization
"""
@task(parameter_file_name=FILE_IN,returns=2)
def SerializeModelParameters_Task(parameter_file_name):
    with open(parameter_file_name,'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())
    model = KratosMultiphysics.Model()
    # parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(model_part_file_name[:-5])
    fake_sample = 0.25
    simulation = SimulationScenario(model,parameters,fake_sample)
    simulation.Initialize()
    serialized_model = KratosMultiphysics.StreamSerializer()
    serialized_model.Save("ModelSerialization",simulation.model)
    serialized_parameters = KratosMultiphysics.StreamSerializer()
    serialized_parameters.Save("ParametersSerialization",simulation.project_parameters)
    # pickle dataserialized_data
    pickled_model = pickle.dumps(serialized_model, 2) # second argument is the protocol and is NECESSARY (according to pybind11 docs)
    pickled_parameters = pickle.dumps(serialized_parameters, 2)
    print("\n","#"*50," SERIALIZATION COMPLETED ","#"*50,"\n")
    return pickled_model,pickled_parameters


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
    qoi = compss_wait_on(qoi)
    print("\nqoi values:\n",qoi)
