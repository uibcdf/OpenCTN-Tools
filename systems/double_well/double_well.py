import argparse
import yaml
import pyunitwizard as puw
import openmm as mm
import openmm.app as app
import openmm.unit as unit
import numpy as np
from tqdm import tqdm

puw.configure.load_library(['pint', 'openmm.unit'])
puw.configure.set_default_form('openmm.unit')

parser = argparse.ArgumentParser(description='Langevin dynamics of a particle in a double well potential.')
parser.add_argument('-i', '--input_file', type=str,
                    help='The input data yaml file')
parser.add_argument('-o', '--output_file', type=str,
                    help='The output npz file')

args = parser.parse_args()

with open(args.input_file, "r") as fff:
    data = yaml.load(fff, Loader=yaml.FullLoader)

n_particles = data['n_particles']
mass = puw.quantity(data['mass'])
temperature = puw.quantity(data['temperature'])
friction = puw.quantity(data['friction'])
Eo = puw.quantity(data['Eo'])
a = puw.quantity(data['a'])
b = puw.quantity(data['b'])
k = puw.quantity(data['k'])
simulation_time = puw.quantity(data['simulation_time'])
saving_time = puw.quantity(data['saving_time'])
integration_timestep = puw.quantity(data['integration_timestep'])
platform_name = data['platform_name']

# System

system = mm.System()

for ii in range(n_particles):
    system.addParticle(mass)

# External potential

force = mm.CustomExternalForce('A*x^4+B*x^2+C*x + D*(y^2+z^2)')
force.addGlobalParameter('A', Eo/(a**4))
force.addGlobalParameter('B', -2.0*Eo/(a**2))
force.addGlobalParameter('C', -b/a)
force.addGlobalParameter('D', k/2.0)

for ii in range(n_particles):
    force.addParticle(ii, [])
_ = system.addForce(force)

# Integrator

integrator = mm.LangevinIntegrator(temperature, friction, integration_timestep)

# Computing platform

platform = mm.Platform.getPlatformByName(platform_name)

# Context

context = mm.Context(system, integrator, platform)

# Initial conditions

initial_positions  = np.zeros([n_particles, 3], np.float32) * unit.angstroms
initial_velocities = np.zeros([n_particles, 3], np.float32) * unit.angstroms/unit.picoseconds

initial_positions[0,0] = a # initial x coordinate in a minimum

context.setPositions(initial_positions)
context.setVelocities(initial_velocities)

# Auxiliary simulation parameters
n_steps_per_period = int(saving_time/integration_timestep)
n_periods = int(simulation_time/saving_time)

# Arrays to store times and positions

times = np.zeros([n_periods], np.float32) * unit.nanoseconds
positions = np.zeros([n_periods, n_particles, 3], np.float32) * unit.angstroms

# Time and positions for time 0

state = context.getState(getPositions=True)
times[0] = state.getTime()
positions[0] = state.getPositions()

# Loop to run the simulation

for ii in tqdm(range(1, n_periods)):
    context.getIntegrator().step(n_steps_per_period)
    state = context.getState(getPositions=True)
    times[ii] = state.getTime()
    positions[ii] = state.getPositions()

np.savez(args.output_file, times = times._value, time_unit=times.unit.get_name(),
         positions = positions._value, length_unit=positions.unit.get_name())

