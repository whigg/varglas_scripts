import varglas.solvers            as solvers
import varglas.physics            as physics
import varglas.model              as model
from varglas.mesh.mesh_factory    import MeshFactory
from varglas.helper               import default_nonlin_solver_params, \
                                         default_config
from fenics                       import *
from time                         import time
from termcolor                    import colored, cprint


t0 = time()

# get the input args :
out_dir = 'dump/linear_model/'
var_dir = 'dump/vars/'
in_dir  = 'dump/test/01/'

mesh   = Mesh(var_dir + 'mesh.xdmf')
Q      = FunctionSpace(mesh, 'CG', 1)
ff     = MeshFunction('size_t', mesh)
cf     = MeshFunction('size_t', mesh)
ff_acc = MeshFunction('size_t', mesh)

S      = Function(Q)
B      = Function(Q)
T_s    = Function(Q)
U_ob   = Function(Q)
adot   = Function(Q)
q_geo  = Function(Q)
u_ob   = Function(Q)
v_ob   = Function(Q)

f = HDF5File(mesh.mpi_comm(), var_dir + 'vars.h5', 'r')

f.read(S,     'S')
f.read(B,     'B')
f.read(T_s,   'T_s')
f.read(U_ob,  'U_ob')
f.read(adot,  'adot')
f.read(q_geo, 'q_geo')
f.read(u_ob,  'u')
f.read(v_ob,  'v')
f.read(ff,    'ff')
f.read(cf,    'cf')
f.read(ff_acc,'ff_acc')

model = model.Model()
model.set_mesh(mesh)
model.set_surface_and_bed(S, B)
model.set_subdomains(ff, cf, ff_acc)
model.initialize_variables()

# specify non-linear solver parameters :
params = default_nonlin_solver_params()
#params['nonlinear_solver']                          = 'snes'
#params['snes_solver']['method']                     = 'newtonls'
#params['snes_solver']['line_search']                = 'basic'
#params['snes_solver']['error_on_nonconvergence']    = False
#params['snes_solver']['absolute_tolerance']         = 1.0
#params['snes_solver']['relative_tolerance']         = 1e-3
#params['snes_solver']['maximum_iterations']         = 20
#params['snes_solver']['linear_solver']              = 'cg'
#params['snes_solver']['preconditioner']             = 'hypre_amg'
params['nonlinear_solver']                          = 'newton'
params['newton_solver']['relaxation_parameter']     = 0.7
params['newton_solver']['relative_tolerance']       = 1e-6
params['newton_solver']['maximum_iterations']       = 16
params['newton_solver']['error_on_nonconvergence']  = False
params['newton_solver']['linear_solver']            = 'cg'
params['newton_solver']['preconditioner']           = 'hypre_amg'
#params['newton_solver']['krylov_solver']['monitor_convergence']  = True
parameters['form_compiler']['quadrature_degree']    = 2
#parameters['krylov_solver']['monitor_convergence']  = True
#parameters['lu_solver']['verbose']                  = True

config = default_config()
config['output_path']                      = out_dir
config['log']                              = True
config['log_history']                      = True
config['coupled']['on']                    = True
config['coupled']['max_iter']              = 10
config['velocity']['newton_params']        = params
config['velocity']['approximation']        = 'fo'#'stokes'
config['velocity']['viscosity_mode']       = 'full'
config['velocity']['vert_solve_method']    = 'mumps'
config['velocity']['calc_pressure']        = True
config['enthalpy']['on']                   = True
config['enthalpy']['solve_method']         = 'mumps'
config['velocity']['init_beta_from_stats'] = True
config['age']['on']                        = False
config['age']['use_smb_for_ela']           = True
config['balance_velocity']['kappa']        = 20.0
config['balance_velocity']['adot']         = adot

model.init_q_geo(model.ghf)
model.init_T_surface(T_s)
model.init_adot(adot)
model.init_U_ob(u_ob, v_ob)
model.init_T(in_dir + 'T.xml')
model.init_W(in_dir + 'W.xml')
model.init_Ubar(in_dir + 'Ubar.xml')
model.init_Mb(in_dir + 'Mb.xml')

# solve the BP model :
F = solvers.SteadySolver(model, config)
File(out_dir + 'beta0.pvd') << model.beta
F.solve()

# calculate total time to compute
tf = time()
s  = tf - t0
m  = s / 60.0
h  = m / 60.0
s  = s % 60
m  = m % 60
if model.MPI_rank == 0:
  s    = "Total time to compute: %02d:%02d:%02d" % (h,m,s)
  text = colored(s, 'red', attrs=['bold'])
  print text


