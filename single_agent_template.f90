module model_t
  use, intrinsic :: iso_fortran_env, only: wp => real64

  use gensys, only: do_gensys
  use fortress, only : fortress_lgss_model
  use fortress_prior_t, only: model_prior => prior
  use fortress_util, only: write_array_to_file

  implicit none

  type, public, extends(fortress_lgss_model) :: model
     integer :: neta
     integer :: k = {k}

   contains
     procedure :: system_matrices
     procedure :: get_decision_rule
  end type model


  interface model
     module procedure new_model
  end interface model


contains

  type(model) function new_model() result(self)

    character(len=144) :: name, datafile, priorfile
    integer :: nobs, T, ns, npara, neps

    name = 'woodford'
    datafile = 'data.txt'
    priorfile = 'prior.txt'

    nobs = 3
    T = 168

    ns = 15
    npara = 17
    neps = 3

    call self%construct_model(name, datafile, priorfile, npara, nobs, T, ns, neps)

    self%neta = 5
    self%t0 = 0
  end function new_model

  subroutine get_decision_rule(self, para, k, TT, RR)

    class(model), intent(inout) :: self
    real(wp), intent(in) :: para(self%npara)
    integer, intent(in) :: k

    real(wp) :: beta,   kappa,   sigma,   alpha,   phidp,   phiy,   rhoxi,   rhoi,   rhoy,   gam,   gamtilde,   phidpbar,   phiybar 

    integer :: i, j

    real(wp) :: GGAM(2,2), Vx(2,2), Vs(2,3), PP(3,3), mm_inv(2,2), ms(2,3)
    real(wp) :: C_k(2,3), A(2,2), sum_mat(2,3), Ast(2,3), mv(2,2), Mbar(2,2), B_i(2,3)
    real(wp) :: mlag(2,2), Nbar(2,2), Av(2,2), Aitilde(2), Bitilde(3), Aibar(2), matpow(2,2), Nbar_power(2,2)

    !real(wp) :: TT(self%ns, self%ns), RR(self%ns, self%neps)
    real(wp) :: TT(15, 15), RR(15, 3)


    beta =  1/(1+para(0+1)/400)
    kappa = para(4+1)
    sigma = para(5+1)
    alpha = 0.75d0 
    phidp = para(6+1)
    phiy =  para(7+1)
    rhoxi = para(11+1)
    rhoi = para(12+1)
    rhoy = para(13+1)
    gam = para(14+1)
    gamtilde = gam
    phidpbar = para(15+1)
    phiybar = para(16+1)

    PP = 0.0d0
    PP(1,1) = rhoy
    PP(2,2) = rhoxi
    PP(3,3) = rhoi



    GGAM = 0.0_wp 
    Vx = 0.0_wp 
    Vs = 0.0_wp 
    GGAM(1,1) = 1-gamtilde
    GGAM(2,2) = 1-gam
    Vx(1,1) = gamtilde/(1-alpha)
    Vx(2,1) = gam*sigma
    Vx(2,2) = gam
    Vs(2,2) = -gam


    mm_inv(1,:) = [1.0d0+sigma*phiy, kappa]
    mm_inv(2,:) = [-sigma*phidp,1.0d0]
    mm_inv = mm_inv/((1.0d0+sigma*phiy)+kappa*sigma*phidp)

    ms(1,:) = [-kappa*rhoy**k, 0.0d0, 0.0d0]
    ms(2,:) = [0.0d0, rhoxi**k, -sigma*rhoi**k]
    C_k = matmul(mm_inv, ms)

    mm_inv(1,:) = [1.0d0+sigma*phiy, kappa]
    mm_inv(2,:) = [-sigma*phidp,1.0d0]
    mm_inv = mm_inv/((1.0d0+sigma*phiy)+kappa*sigma*phidp)

    mlag(1,:) =  [beta, 0.0d0]
    mlag(2,:) = [sigma, 1.0d0]
    A = matmul(mm_inv, mlag)
    matpow(1,:) = [1.0d0, 0.0d0]
    matpow(2,:) = [0.0d0, 1.0d0]
    sum_mat = 0.0_wp

    do j = 1, k
       ms(1,:) = [-kappa*rhoy**(j-1), 0.0d0, 0.0d0]
       ms(2,:) = [0.0d0, rhoxi**(j-1)*(1-rhoxi), -sigma*rhoi**(j-1)]

       B_i = matmul(mm_inv, ms)
       sum_mat = sum_mat + matmul(matpow, B_i)
       matpow = matmul(matpow, A)
    end do
    Ast = matmul(matpow, C_k) + sum_mat

    mm_inv(1,:) = [1.0d0+sigma*phiybar, kappa]
    mm_inv(2,:) = [-sigma*phidpbar,1.0d0]
    mm_inv = mm_inv/((1.0d0+sigma*phiybar)+kappa*sigma*phidpbar) 

    mv(1,:) = [(1.0d0-alpha)*beta, 0.0d0]
    mv(2,:) = [0.0d0,1.0d0]
    Mbar = matmul(mm_inv, mv)

    mlag(1,:) = [beta, 0.0d0]
    mlag(2,:) = [sigma, 1.0d0]
    Nbar = matmul(mm_inv, mlag)
    Nbar_power(1,:) = [1.0d0, 0.0d0]
    Nbar_power(2,:) = [0.0d0, 1.0d0]
    do i = 1,k
       Nbar_power = matmul(Nbar, Nbar_power)
    end do
    Av = matmul(Nbar_power, Mbar)

    TT = 0.0_wp
    TT(1:2,1:2) = matmul(Av , Vx )

    TT(1:2,7:8) = matmul(Av , GGAM)
    TT(1:2,12:14) = matmul(Av, Vs) + matmul(Ast, PP)
    TT(7:8,1:2) = Vx
    TT(7:8,7:8) = GGAM
    TT(7:8,12:14) = Vs
    TT(12:14,12:14) = PP

    TT(3:4,12:14) = matmul(Ast, PP)
    TT(5:6,1:2) = matmul(Av, Vx)
    TT(5:6,7:8) = matmul(Av, GGAM)
    TT(5:6,12:14) = matmul(Av, Vs)


    Aitilde = [phidp, phiy]
    Aibar = [phidpbar, phiybar]
    Bitilde = [0.0d0, 0.0d0, 1.0d0]

    TT(10,12:14) = matmul( Aitilde , matmul(Ast , PP)) + matmul(Bitilde , PP)
    TT(11,1:2) = matmul(Aibar , matmul( Av , Vx ))
    TT(11,7:8) = matmul(Aibar , matmul(Av , GGAM))
    TT(11,12:14) = matmul(Aibar , matmul(Av , Vs ))
    TT(9,1:2) = TT(11,1:2)
    TT(9,7:8) = TT(11,7:8)
    TT(9,12:14) = TT(11,12:14) + TT(10,12:14)

    TT(15,2) = 1.0d0

    RR = 0.0_wp
    RR(1:2,:) = Ast
    do i = 12,14
       RR(i,i-11) = 1.0d0
    end do
    RR(3:4,:) = Ast
    RR(10,:) = matmul(Aitilde , Ast) + Bitilde
    RR(9,:) = matmul(Aitilde , Ast) + Bitilde    



  end subroutine get_decision_rule

  subroutine system_matrices(self, para, error)

    class(model), intent(inout) :: self
    real(wp), intent(in) :: para(self%npara)

    integer, intent(out) :: error 

    integer :: info

    real(wp) :: beta,   kappa,   sigma,   alpha,   phidp,   phiy,   rhoxi,   rhoi,   rhoy,   gam,   gamtilde,   phidpbar,   phiybar 

    integer :: i, j

    call self%get_decision_rule(para, self%k, self%TT, self%RR)

    self%QQ = 0.0d0
    self%ZZ = 0.0d0
    self%HH = 0.0d0

    self%QQ(1, 1) = para(9)**2.0d0
    self%QQ(2, 2) = para(10)**2.0d0
    self%QQ(3, 3) = para(11)**2.0d0

    !p1 = 0.00_wp
    !p2 = 0.00_wp
    !p3 = 0.00_wp

    self%DD(1) = para(3)
    self%DD(2) = para(2)
    self%DD(3) = para(1) + para(2)

    self%ZZ(1,2)  =  1.0d0 !* p1 
    self%ZZ(1,15) = -1.0d0 !* p1 
    self%ZZ(2,1)  =  4.0d0 !* p1 
    self%ZZ(3,9)  =  4.0d0 !* p1 

    error=0

    !call write_array_to_file('RR.txt', self%RR)
    !call write_array_to_file('TT.txt', self%TT)


  end subroutine system_matrices


end module model_t
