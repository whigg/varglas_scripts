varglas_scripts
===============

Scripts for the glacier simulator VarGlaS

Precondtioner for krylov solver :
---------------------------------
The only preconditioner that worked (including no preconditioner) is 'hypre_amg'.


24 cores :
==========

FEniCS Newton solver evaluation :
------------------------------------------------

24 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg', step length 0.7:


| Krylov Solver | 33484 nodes | 538208 nodes  | 759264 nodes  
|---------------|-------------|---------------|---------------
| 'cg'          | 00:40       | 16:27 - 16:37 | 37:10
| 'gmres'       | 00:42       | KSP DIVERGED  | 06:11:38
| 'minres'      | 00:41       | 17:43 - 17:34 | 37:18
| 'tfqmr'       | 00:46       | KSP DIVERGED  | KSP DIVERGED
| 'richardson'  | 11:03       | KSP DIVERGED  | --:--
| 'bicgstab'    | 00:45       | KSP DIVERGED  | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| 00:33       | oo:oo        | oo:oo

SNES Newton line search ('newtonls') basic solver evaluation :
--------------------------------------------------------------

24 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes  | 759264 nodes  
|---------------|-------------|---------------|---------------
| 'cg'          | 00:33       | 12:33         | --:--
| 'gmres'       | 00:31       | 01:19:31      | --:--
| 'minres'      | 00:32       | 12:57         | --:--
| 'tfqmr'       | 00:34       | 02:55:23      | --:--
| 'richardson'  | 05:17       | 02:10:31      | --:--
| 'bicgstab'    | 00:36       | --:--         | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| --:--       | --:--        | --:--

SNES Newton line search ('newtonls') backtracking solver evaluation :
---------------------------------------------------------------------

24 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes  | 759264 nodes  
|---------------|-------------|---------------|---------------
| 'cg'          | --:--       | --:--         | --:--
| 'gmres'       | --:--       | --:--         | --:--
| 'minres'      | --:--       | --:--         | --:--
| 'tfqmr'       | --:--       | --:--         | --:--
| 'richardson'  | --:--       | --:--         | --:--
| 'bicgstab'    | --:--       | --:--         | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| --:--       | --:--        | --:--

SNES Newton trust region ('newtontr') solver evaluation :
---------------------------------------------------------

24 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes  | 759264 nodes  
|---------------|-------------|---------------|---------------
| 'cg'          | --:--       | --:--         | --:--
| 'gmres'       | --:--       | --:--         | --:--
| 'minres'      | --:--       | --:--         | --:--
| 'tfqmr'       | --:--       | --:--         | --:--
| 'richardson'  | --:--       | --:--         | --:--
| 'bicgstab'    | --:--       | --:--         | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| --:--       | --:--        | --:--


28 cores :
==========

FEniCS Newton solver evaluation :
------------------------------------------------

28 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg', step length 0.7:


| Krylov Solver | 33484 nodes | 538208 nodes  | 759264 nodes  
|---------------|-------------|---------------|---------------
| 'cg'          | --:--       | --:--         | --:--
| 'gmres'       | --:--       | --:--         | --:--
| 'minres'      | --:--       | --:--         | --:--
| 'tfqmr'       | --:--       | --:--         | --:--
| 'richardson'  | --:--       | --:--         | --:--
| 'bicgstab'    | --:--       | --:--         | --:--

SNES Newton line search ('newtonls') basic solver evaluation :
--------------------------------------------------------------

28 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes | 759264 nodes  
|---------------|-------------|--------------|---------------
| 'cg'          | 00:19       | vv:oo        | --:--
| 'gmres'       | 00:20       | --:--        | --:--
| 'minres'      | 00:20       | --:--        | --:--
| 'tfqmr'       | 00:22       | --:--        | --:--
| 'richardson'  | 04:54       | --:--        | --:--
| 'bicgstab'    | 00:22       | --:--        | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| --:--       | --:--        | --:--

SNES Newton line search ('newtonls') backtracking solver evaluation :
---------------------------------------------------------------------

28 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes | 759264 nodes  
|---------------|-------------|--------------|---------------
| 'cg'          | 00:26       | vv:oo        | --:--
| 'gmres'       | 00:27       | vv:oo        | --:--
| 'minres'      | 00:26       | vv:oo        | --:--
| 'tfqmr'       | 00:28       | 03:45:32     | --:--
| 'richardson'  | 07:28       | vv:oo        | --:--
| 'bicgstab'    | 00:29       | vv:oo        | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| 00:30       | oo:oo        | oo:oo

SNES Newton trust region ('newtontr') solver evaluation :
---------------------------------------------------------

28 cores, BP momentum with 5 thermomechanically coupled Picard iterations, preconditioner 'hypre_amg':


| Krylov Solver | 33484 nodes | 538208 nodes | 759264 nodes  
|---------------|-------------|--------------|---------------
| 'cg'          | 00:45       | 16:35        | vv:oo
| 'gmres'       | 00:43       | 16:11        | vv:oo
| 'minres'      | 00:44       | vv:oo        | --:--
| 'tfqmr'       | 00:43       | 16:41        | --:--
| 'richardson'  | 00:47       | 21:01        | --:--
| 'bicgstab'    | 00:45       | vv:oo        | --:--

Using the 'mumps' direct solver,

| 33484 nodes | 538208 nodes | 759264 nodes  
|-------------|--------------|---------------
| --:--       | --:--        | --:--



