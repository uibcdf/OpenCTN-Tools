#!/usr/bin/env python

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

# Parsing cli arguments

parser = argparse.ArgumentParser(description='Langevin dynamics of a particle in a double well potential.')
parser.add_argument('-i', '--input_file', type=str,
                    help='The input data yaml file')
parser.add_argument('-o', '--output_file', type=str,
                    help='The output file')

args = parser.parse_args()

# Reading the input parameters

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

# Trajectory file

fff = open(args.output_file,'w')
fff.write("# time [nanoseconds]    x [angstroms]   y [angstroms]   z [angstroms]\n")

# Time and positions for time 0

state = context.getState(getPositions=True)
time = state.getTime()
position = state.getPositions(asNumpy=True)

t = puw.get_value(time, to_unit='nanoseconds')
x = puw.get_value(position[0,0], to_unit='angstroms')
y = puw.get_value(position[0,1], to_unit='angstroms')
z = puw.get_value(position[0,2], to_unit='angstroms')

fff.write(f"{t} {x} {y} {z}\n")

# Loop to run the simulation

for ii in tqdm(range(1, n_periods)):

    context.getIntegrator().step(n_steps_per_period)
    state = context.getState(getPositions=True)
    time = state.getTime()
    position = state.getPositions(asNumpy=True)

    t = puw.get_value(time, to_unit='nanoseconds')
    x = puw.get_value(position[0,0], to_unit='angstroms')
    y = puw.get_value(position[0,1], to_unit='angstroms')
    z = puw.get_value(position[0,2], to_unit='angstroms')

    fff.write(f"{t} {x} {y} {z}\n")

fff.close()

