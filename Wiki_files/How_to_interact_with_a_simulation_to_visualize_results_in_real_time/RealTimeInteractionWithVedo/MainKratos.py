import KratosMultiphysics
import KratosMultiphysics.RomApplication as romapp
from KratosMultiphysics.RomApplication.structural_mechanics_analysis_rom import StructuralMechanicsAnalysisROM
from KratosMultiphysics.assign_scalar_variable_to_conditions_process import AssignScalarVariableToConditionsProcess
import json

#Import visualization tool
import vedo

#Slider class
class Slider():
    def __init__(self, InitialValue):
        self.value = InitialValue

    def GenericSlider(self,widget, event):
        value = widget.GetRepresentation().GetValue()*1e6
        self.value = value


"""
For user-scripting it is intended that a new class is derived
from StructuralMechanicsAnalysis to do modifications
"""

class InteractiveSimulation(StructuralMechanicsAnalysisROM):

    def __init__(self,model,project_parameters):
        super().__init__(model,project_parameters)

        ######### GUI attributes
        self.Continue = True
        self.timestep= 0
        self.slider1 = Slider(0)
        self.Plot = vedo.Plotter(title="Simulation Results",interactive=False)
        self.Plot.addSlider2D(self.slider1.GenericSlider, -200, 400 , value = 0, pos=3, title="Pressure (MPa)")
        self.Plot += vedo.Text2D('Move the slider to change the Pressure on the Face of the Bunny', s=1.2)
        self.PauseButton = self.Plot.addButton(
                self.PauseButtonFunc,
                pos=(0.9, .9),  # x,y fraction from bottom left corner
                states=["PAUSE", "CONTINUE"],
                c=["w", "w"],
                bc=["b", "g"],  # colors of states
                font="courier",   # arial, courier, times
                size=25,
                bold=True,
                italic=False,
                )

        self.StopButton = self.Plot.addButton(
                self.StopButtonFunc,
                pos=(0.1, .9),  # x,y fraction from bottom left corner
                states=["STOP"],
                c=["w"],
                bc=["r"],  # colors of states
                font="courier",   # arial, courier, times
                size=25,
                bold=True,
                italic=False,
                )
        self.Plot.show()

    def PauseButtonFunc(self):
        vedo.printc(self.PauseButton.status(), box="_", dim=True)
        if self.PauseButton.status() == "PAUSE":
            self.Plot.interactive = True
        else:
            self.Plot.interactive = False
        self.PauseButton.switch() # change to next status

    def StopButtonFunc(self):
        vedo.printc(self.StopButton.status(), box="_", dim=True)
        if self.StopButton.status() == "STOP":
            self.Finalize()
            self.Continue = False

    def ModifyInitialGeometry(self):
        super().ModifyInitialGeometry()
        computing_model_part = self._solver.GetComputingModelPart()
        ## Adding the weights to the corresponding elements
        with open('ElementsAndWeights.json') as f:
            HR_data = json.load(f)
            for key in HR_data["Elements"].keys():
                computing_model_part.GetElement(int(key)+1).SetValue(romapp.HROM_WEIGHT, HR_data["Elements"][key])
            for key in HR_data["Conditions"].keys():
                computing_model_part.GetCondition(int(key)+1).SetValue(romapp.HROM_WEIGHT, HR_data["Conditions"][key])


    def FinalizeSolutionStep(self):
        super().FinalizeSolutionStep()
        if self.timestep>1.5:
            if self.timestep==2:
                self.a_mesh = vedo.load(f'./vtk_output/VISUALIZE_HROM_0_{self.timestep}.vtk').tomesh(fill=True, shrink=1)
                displs = self.a_mesh.getPointArray("DISPLACEMENT")

            if self.timestep>2:
                b_mesh = vedo.load(f'./vtk_output/VISUALIZE_HROM_0_{self.timestep}.vtk').tomesh(fill=True, shrink=1)
                newpoints = b_mesh.points()
                displs = b_mesh.getPointArray("DISPLACEMENT")
                self.a_mesh.points(newpoints+displs)

            self.a_mesh.pointColors(vedo.mag(displs), cmap='jet',vmin = 0, vmax = 0.009).addScalarBar()
            self.a_mesh.show(axes=1, viewup='z')
        self.timestep +=1

    def KeepAdvancingSolutionLoop(self):
        return self.Continue

    def ApplyBoundaryConditions(self):
        super().ApplyBoundaryConditions()
        Pressure = self.slider1.value
        print(f'Pressure is {Pressure} Pa')
        PressureSettings = KratosMultiphysics.Parameters("""
        {
            "model_part_name" : "Structure.COMPUTE_HROM.SurfacePressure3D_Pressure_on_surfaces_Auto4",
            "variable_name"   : "POSITIVE_FACE_PRESSURE",
            "interval"        : [0.0,"End"]
        }
        """
        )
        PressureSettings.AddEmptyValue("value").SetDouble(Pressure)
        AssignScalarVariableToConditionsProcess(self.model, PressureSettings).ExecuteInitializeSolutionStep()


if __name__ == "__main__":
    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())
    model = KratosMultiphysics.Model()
    simulation = InteractiveSimulation(model,parameters)
    simulation.Run()

