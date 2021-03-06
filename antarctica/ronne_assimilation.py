import sys
import varglas.solvers            as solvers
import varglas.physical_constants as pc
import varglas.model              as model
from varglas.mesh.mesh_factory    import MeshFactory
from varglas.data.data_factory    import DataFactory
from varglas.helper               import default_nonlin_solver_params
from varglas.io                   import DataInput, DataOutput
from fenics                       import *

# get the input args :
i = int(sys.argv[2])           # assimilation number
dir_b = sys.argv[1] + '/0'     # directory to save

# set the output directory :
out_dir = dir_b + str(i) + '/'
in_dir  = 'vars/'

set_log_active(True)

thklim = 1.0

measures  = DataFactory.get_ant_measures(res=450)
bedmap1   = DataFactory.get_bedmap1(thklim=thklim)
bedmap2   = DataFactory.get_bedmap2(thklim=thklim)

mesh = MeshFactory.get_ronne_3D_50H()

dm  = DataInput(measures, mesh=mesh)
db1 = DataInput(bedmap1,  mesh=mesh)
db2 = DataInput(bedmap2,  mesh=mesh)

db2.data['B'] = db2.data['S'] - db2.data['H']
db2.set_data_val('H', 32767, thklim)
db2.data['S'] = db2.data['B'] + db2.data['H']

H      = db2.get_nearest_expression("H")
S      = db2.get_nearest_expression("S")
B      = db2.get_nearest_expression("B")
M      = db2.get_nearest_expression("mask")
T_s    = db1.get_nearest_expression("srfTemp")
q_geo  = db1.get_nearest_expression("q_geo")
adot   = db1.get_nearest_expression("adot")
U_ob   = dm.get_projection("U_ob", near=True)
u      = dm.get_nearest_expression("vx")
v      = dm.get_nearest_expression("vy")

model = model.Model()
model.set_mesh(mesh)
model.set_geometry(S, B,deform=True)
model.calculate_boundaries(mask=M, adot=adot)
model.set_parameters(pc.IceParameters())
model.initialize_variables()

# constraints on optimization for beta :
class Bounds_max(Expression):
  def eval(self, values, x):
    if M(x[0], x[1], x[2]) > 0:
      values[0] = 2 * DOLFIN_EPS
    else:
      values[0] = 100000.0

# initial friction coef :
class Beta_0(Expression):
  def eval(self, values, x):
    if M(x[0], x[1], x[2]) > 0:
      values[0] = DOLFIN_EPS
    else:
      values[0] = 4

beta_min = interpolate(Constant(0.0), model.Q)
beta_max = interpolate(Bounds_max(element = model.Q.ufl_element()), model.Q)

# specifify non-linear solver parameters :
nonlin_solver_params = default_nonlin_solver_params()
nonlin_solver_params['newton_solver']['relaxation_parameter']    = 0.7
nonlin_solver_params['newton_solver']['relative_tolerance']      = 1e-3
nonlin_solver_params['newton_solver']['maximum_iterations']      = 16
nonlin_solver_params['newton_solver']['error_on_nonconvergence'] = False
nonlin_solver_params['newton_solver']['linear_solver']           = 'mumps'
nonlin_solver_params['newton_solver']['preconditioner']          = 'default'
parameters['form_compiler']['quadrature_degree']                 = 2


config = { 'mode'                         : 'steady',
           't_start'                      : None,
           't_end'                        : None,
           'time_step'                    : None,
           'output_path'                  : out_dir,
           'wall_markers'                 : [],
           'periodic_boundary_conditions' : False,
           'log'                          : True,
           'coupled' : 
           { 
             'on'                  : True,
             'inner_tol'           : 0.0,
             'max_iter'            : 2
           },
           'velocity' : 
           { 
             'on'                  : True,
             'newton_params'       : nonlin_solver_params,
             'viscosity_mode'      : 'full',
             'b_linear'            : None,
             'use_T0'              : True,
             'T0'                  : model.T_w - 15.0,
             'A0'                  : 1e-16,
             'beta'                : 0.0,
             'init_beta_from_U_ob' : True,
             'U_ob'                : U_ob,
             'r'                   : 0.0,
             'E'                   : 1.0,
             'approximation'       : 'fo',
             'boundaries'          : 'user_defined',
             'u_lat_boundary'      : u,
             'v_lat_boundary'      : v,
             'log'                 : True
           },
           'enthalpy' : 
           { 
             'on'                  : True,
             'use_surface_climate' : False,
             'T_surface'           : T_s,
             'q_geo'               : q_geo,
             'lateral_boundaries'  : None,
             'log'                 : True
           },
           'free_surface' :
           { 
             'on'                  : False,
             'lump_mass_matrix'    : True,
             'thklim'              : thklim,
             'use_pdd'             : False,
             'observed_smb'        : adot,
           },  
           'age' : 
           { 
             'on'                  : False,
             'use_smb_for_ela'     : True,
             'ela'                 : 750,
           },
           'surface_climate' : 
           { 
             'on'                  : False,
             'T_ma'                : None,
             'T_ju'                : None,
             'beta_w'              : None,
             'sigma'               : None,
             'precip'              : None
           },
           'adjoint' :
           { 
             'alpha'               : 1e-7,
             'gamma1'              : 1.0,
             'gamma2'              : 10.0,
             'max_fun'             : 20,
             'objective_function'  : 'log_lin_hybrid',
             'bounds'              : (0, 0),
             'control_variable'    : model.beta,
             'regularization_type' : 'Tikhonov'
           }}

if i !=0:
  #config['velocity']['approximation']   = 'stokes'
  config['velocity']['use_T0']           = False
  File(dir_b + str(i-1) + '/T.xml')     >> model.T

F = solvers.SteadySolver(model, config)
File(out_dir + 'beta_0.pvd') << model.beta
F.solve()

File(out_dir + 'U_ob.pvd') << U_ob
File(out_dir + 'ff.pvd')   << model.ff

b_shf = project(model.b, model.Q)
b_gnd = b_shf.copy()
model.print_min_max(b_shf, 'b')
b_min = b_shf.vector().min()/10.0
b_max = b_shf.vector().max()*10.0

model.b = project(model.b, model.Q)

File(out_dir + 'b_0.pvd') << model.b

params = config['velocity']['newton_params']['newton_solver']
params['relaxation_parameter']         = 0.5
params['maximum_iterations']           = 16
config['velocity']['viscosity_mode']   = 'shelf_control'
#config['velocity']['viscosity_mode']   = 'linear'
#config['velocity']['viscosity_mode']   = 'b_control'
config['velocity']['b']                = model.b
config['velocity']['b_linear']         = model.eta
config['velocity']['b_linear_shf']     = b_shf
config['velocity']['b_linear_gnd']     = b_gnd
config['enthalpy']['on']               = False
config['surface_climate']['on']        = False
config['coupled']['on']                = False
config['velocity']['use_T0']           = False
config['adjoint']['alpha']             = [1e-7, 0]
config['adjoint']['bounds']            = [(beta_min, beta_max), (b_min, b_max)]
config['adjoint']['control_variable']  = [model.beta, b_shf]

A = solvers.AdjointSolver(model, config)
A.set_target_velocity(u=u, v=v)
A.solve()

File(out_dir + 'T.xml')       << model.T
File(out_dir + 'S.xml')       << model.S
File(out_dir + 'B.xml')       << model.B
File(out_dir + 'u.xml')       << project(model.u, model.Q) 
File(out_dir + 'v.xml')       << project(model.v, model.Q) 
File(out_dir + 'w.xml')       << model.w 
File(out_dir + 'beta.xml')    << model.beta
File(out_dir + 'eta.xml')     << project(model.eta, model.Q)
File(out_dir + 'b.pvd')       << project(model.b,   model.Q)
File(out_dir + 'b_shf.pvd')   << model.b_shf
#File(out_dir + 'b_gnd.pvd')   << model.b_shf

#XDMFFile(mesh.mpi_comm(), out_dir + 'mesh.xdmf')   << model.mesh
#
## save the state of the model :
#if i !=0: rw = 'a'
#else:     rw = 'w'
#f = HDF5File(mesh.mpi_comm(), out_dir + '3D_5H_stokes.h5', rw)
#f.write(model.mesh,  'mesh')
#f.write(model.beta,  'beta')
#f.write(model.Mb,    'Mb')
#f.write(model.T,     'T')
#f.write(model.S,     'S')
#f.write(model.B,     'B')
#f.write(model.U,     'U')
#f.write(model.eta,   'eta')



