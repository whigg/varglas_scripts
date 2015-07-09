from fenics                    import *
from varglas.solvers           import HybridTransientSolver
from varglas.helper            import default_config
from varglas.model             import Model

set_log_active(False)

in_dir  = 'dump2/stats_trough_Ubar_dirU/'
out_dir = 'dump/stats_trough_test_stats/'

parameters['form_compiler']['quadrature_degree'] = 2
parameters['form_compiler']['precision']         = 30
#parameters['form_compiler']['optimize']          = True
parameters['form_compiler']['cpp_optimize']      = True
parameters['form_compiler']['representation']    = 'quadrature'

mesh = Mesh('meshes/circle_mesh.xml')

thklim = 1.0
L      = 800000.

for x in mesh.coordinates():
  # transform x :
  x[0]  = x[0]  * L
  # transform y :
  x[1]  = x[1]  * L

config = default_config()
config['log']                          = True
config['log_history']                  = True
config['mode']                         = 'transient'
config['model_order']                  = 'L1L2'
config['output_path']                  = out_dir
config['t_start']                      = 0.0
config['t_end']                        = 5000.0
config['time_step']                    = 10.0
config['periodic_boundary_conditions'] = False
config['velocity']['poly_degree']      = 2
config['enthalpy']['on']               = True
config['enthalpy']['N_T']              = 8
config['free_surface']['on']           = True
config['free_surface']['thklim']       = thklim
config['velocity']['transient_beta']   = 'stats'

model = Model(config)
model.set_mesh(mesh)

model.rhoi = 910.0

S = Function(model.Q)
B = Function(model.Q)

File(in_dir + 'S.xml') >> S
File(in_dir + 'B.xml') >> B

class Adot(Expression):
  Rel = 450000
  s   = 1e-5
  def eval(self,values,x):
    values[0] = min(0.5,self.s*(self.Rel-sqrt(x[0]**2 + x[1]**2)))
adot = Adot(element=model.Q.ufl_element())

class SurfaceTemperature(Expression):
  t    = 0.0
  Tmin = 238.15
  St   = 1.67e-5
  def eval(self,values,x):
    values[0] = self.Tmin + self.St*sqrt(x[0]**2 + x[1]**2)
T_s = SurfaceTemperature(element=model.Q.ufl_element())

model.set_surface_and_bed(S, B)
model.initialize_variables()

model.init_adot(adot)
model.init_T_surface(T_s)
model.init_H_bounds(thklim, 1e4)
model.init_q_geo(model.ghf)
model.init_H(in_dir + 'H.xml')
#model.init_beta(in_dir + 'beta.xml')
model.init_beta_stats('Ubar')

model.save_pvd(model.S,    'S')
model.save_pvd(model.B,    'B')
model.save_pvd(model.beta, 'beta')

model.eps_reg = 1e-10

T = HybridTransientSolver(model, config)
T.solve()

File(out_dir + 'Ts.xml')      << model.Ts
File(out_dir + 'Tb.xml')      << model.Tb
File(out_dir + 'Mb.xml')      << model.Mb
File(out_dir + 'H.xml')       << model.H
File(out_dir + 'S.xml')       << model.S
File(out_dir + 'B.xml')       << model.B
File(out_dir + 'u_s.xml')     << model.u_s
File(out_dir + 'v_s.xml')     << model.v_s
File(out_dir + 'w_s.xml')     << model.w_s
File(out_dir + 'u_b.xml')     << model.u_b
File(out_dir + 'v_b.xml')     << model.v_b
File(out_dir + 'w_b.xml')     << model.w_b
File(out_dir + 'Ubar.xml')    << model.Ubar
File(out_dir + 'beta.xml')    << model.beta



