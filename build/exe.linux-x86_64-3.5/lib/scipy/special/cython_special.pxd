# This file is automatically generated by _generate_pyx.py.
# Do not edit manually!

ctypedef fused Dd_number_t:
    double complex
    double

ctypedef fused dfg_number_t:
    double
    float
    long double

ctypedef fused dl_number_t:
    double
    long

cdef void hyp1f2(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cpdef Dd_number_t eval_gegenbauer(dl_number_t x0, double x1, Dd_number_t x2) nogil
cdef void it2j0y0(double x0, double *y0, double *y1) nogil
cpdef double yn(dl_number_t x0, double x1) nogil
cdef void it2i0k0(double x0, double *y0, double *y1) nogil
cpdef double complex wofz(double complex x0) nogil
cpdef double gammaln(double x0) nogil
cpdef Dd_number_t eval_sh_chebyt(dl_number_t x0, Dd_number_t x1) nogil
cpdef double pseudo_huber(double x0, double x1) nogil
cpdef double ncfdtridfd(double x0, double x1, double x2, double x3) nogil
cdef void kelvin(double x0, double complex *y0, double complex *y1, double complex *y2, double complex *y3) nogil
cpdef double betainc(double x0, double x1, double x2) nogil
cpdef double gammainc(double x0, double x1) nogil
cpdef Dd_number_t rgamma(Dd_number_t x0) nogil
cpdef double nctdtrinc(double x0, double x1, double x2) nogil
cpdef double chndtrinc(double x0, double x1, double x2) nogil
cpdef dfg_number_t logit(dfg_number_t x0) nogil
cpdef double i1(double x0) nogil
cpdef double stdtr(double x0, double x1) nogil
cpdef double mathieu_a(double x0, double x1) nogil
cpdef double ellipkinc(double x0, double x1) nogil
cpdef double gammasgn(double x0) nogil
cpdef double poch(double x0, double x1) nogil
cpdef double ker(double x0) nogil
cpdef Dd_number_t hyp0f1(double x0, Dd_number_t x1) nogil
cpdef Dd_number_t kve(double x0, Dd_number_t x1) nogil
cpdef double nbdtrin(double x0, double x1, double x2) nogil
cpdef double k1e(double x0) nogil
cpdef dfg_number_t expit(dfg_number_t x0) nogil
cpdef Dd_number_t psi(Dd_number_t x0) nogil
cdef void sici(Dd_number_t x0, Dd_number_t *y0, Dd_number_t *y1) nogil
cpdef double kn(dl_number_t x0, double x1) nogil
cpdef double nctdtridf(double x0, double x1, double x2) nogil
cpdef Dd_number_t xlog1py(Dd_number_t x0, Dd_number_t x1) nogil
cpdef Dd_number_t loggamma(Dd_number_t x0) nogil
cpdef Dd_number_t erfi(Dd_number_t x0) nogil
cpdef double bdtr(dl_number_t x0, dl_number_t x1, double x2) nogil
cpdef Dd_number_t eval_sh_chebyu(dl_number_t x0, Dd_number_t x1) nogil
cdef void mathieu_modsem2(double x0, double x1, double x2, double *y0, double *y1) nogil
cpdef double pdtrc(dl_number_t x0, double x1) nogil
cpdef double hyperu(double x0, double x1, double x2) nogil
cdef void airye(Dd_number_t x0, Dd_number_t *y0, Dd_number_t *y1, Dd_number_t *y2, Dd_number_t *y3) nogil
cpdef double lpmv(double x0, double x1, double x2) nogil
cpdef Dd_number_t eval_jacobi(dl_number_t x0, double x1, double x2, Dd_number_t x3) nogil
cpdef double stdtrit(double x0, double x1) nogil
cdef void modfresnelp(double x0, double complex *y0, double complex *y1) nogil
cpdef double kolmogi(double x0) nogil
cpdef Dd_number_t hyp1f1(double x0, double x1, Dd_number_t x2) nogil
cpdef double agm(double x0, double x1) nogil
cpdef double fdtrc(double x0, double x1, double x2) nogil
cdef void ellipj(double x0, double x1, double *y0, double *y1, double *y2, double *y3) nogil
cpdef double nbdtrik(double x0, double x1, double x2) nogil
cpdef double btdtrib(double x0, double x1, double x2) nogil
cpdef double complex wrightomega(double complex x0) nogil
cpdef double bdtrin(double x0, double x1, double x2) nogil
cpdef double cosdg(double x0) nogil
cpdef double fdtri(double x0, double x1, double x2) nogil
cpdef Dd_number_t erfcx(Dd_number_t x0) nogil
cpdef double keip(double x0) nogil
cpdef double complex hankel2(double x0, double complex x1) nogil
cdef void itairy(double x0, double *y0, double *y1, double *y2, double *y3) nogil
cpdef double fdtr(double x0, double x1, double x2) nogil
cpdef double ncfdtr(double x0, double x1, double x2, double x3) nogil
cpdef Dd_number_t kv(double x0, Dd_number_t x1) nogil
cpdef double it2struve0(double x0) nogil
cpdef double radian(double x0, double x1, double x2) nogil
cpdef double k0(double x0) nogil
cpdef double betaincinv(double x0, double x1, double x2) nogil
cdef void pbvv(double x0, double x1, double *y0, double *y1) nogil
cpdef double stdtridf(double x0, double x1) nogil
cpdef double k0e(double x0) nogil
cpdef double kei(double x0) nogil
cpdef double ellipe(double x0) nogil
cdef void pro_rad2(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cpdef double bdtri(dl_number_t x0, dl_number_t x1, double x2) nogil
cpdef double exp10(double x0) nogil
cpdef double complex hankel1(double x0, double complex x1) nogil
cpdef double inv_boxcox(double x0, double x1) nogil
cpdef Dd_number_t gamma(Dd_number_t x0) nogil
cpdef double chdtrc(double x0, double x1) nogil
cpdef double round(double x0) nogil
cpdef double itstruve0(double x0) nogil
cpdef double itmodstruve0(double x0) nogil
cpdef Dd_number_t eval_genlaguerre(dl_number_t x0, double x1, Dd_number_t x2) nogil
cpdef double cbrt(double x0) nogil
cdef void obl_rad1(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cdef void fresnel(Dd_number_t x0, Dd_number_t *y0, Dd_number_t *y1) nogil
cpdef Dd_number_t eval_legendre(dl_number_t x0, Dd_number_t x1) nogil
cpdef double besselpoly(double x0, double x1, double x2) nogil
cpdef double k1(double x0) nogil
cdef void iti0k0(double x0, double *y0, double *y1) nogil
cpdef Dd_number_t expm1(Dd_number_t x0) nogil
cpdef Dd_number_t jv(double x0, Dd_number_t x1) nogil
cpdef Dd_number_t iv(double x0, Dd_number_t x1) nogil
cpdef Dd_number_t ive(double x0, Dd_number_t x1) nogil
cpdef double bdtrik(double x0, double x1, double x2) nogil
cpdef double btdtr(double x0, double x1, double x2) nogil
cdef void itj0y0(double x0, double *y0, double *y1) nogil
cpdef Dd_number_t xlogy(Dd_number_t x0, Dd_number_t x1) nogil
cpdef double chndtr(double x0, double x1, double x2) nogil
cdef void hyp2f0(double x0, double x1, double x2, dl_number_t x3, double *y0, double *y1) nogil
cpdef double beip(double x0) nogil
cdef void pbdv(double x0, double x1, double *y0, double *y1) nogil
cpdef double rel_entr(double x0, double x1) nogil
cpdef double ellipeinc(double x0, double x1) nogil
cpdef Dd_number_t exp1(Dd_number_t x0) nogil
cpdef double gdtria(double x0, double x1, double x2) nogil
cdef void pro_ang1_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cdef void pbwa(double x0, double x1, double *y0, double *y1) nogil
cpdef double betaln(double x0, double x1) nogil
cpdef double complex hankel2e(double x0, double complex x1) nogil
cpdef double btdtri(double x0, double x1, double x2) nogil
cpdef double pdtri(dl_number_t x0, double x1) nogil
cpdef Dd_number_t yve(double x0, Dd_number_t x1) nogil
cpdef double beta(double x0, double x1) nogil
cpdef double tandg(double x0) nogil
cpdef Dd_number_t eval_sh_legendre(dl_number_t x0, Dd_number_t x1) nogil
cpdef Dd_number_t eval_chebyc(dl_number_t x0, Dd_number_t x1) nogil
cpdef Dd_number_t eval_chebyu(dl_number_t x0, Dd_number_t x1) nogil
cdef void mathieu_modsem1(double x0, double x1, double x2, double *y0, double *y1) nogil
cpdef double berp(double x0) nogil
cpdef Dd_number_t eval_chebyt(dl_number_t x0, Dd_number_t x1) nogil
cpdef double gdtrc(double x0, double x1, double x2) nogil
cpdef Dd_number_t spence(Dd_number_t x0) nogil
cdef void obl_rad2(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cdef void shichi(Dd_number_t x0, Dd_number_t *y0, Dd_number_t *y1) nogil
cpdef double tklmbda(double x0, double x1) nogil
cpdef double complex sph_harm(dl_number_t x0, dl_number_t x1, double x2, double x3) nogil
cdef void obl_rad1_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cpdef double nctdtr(double x0, double x1, double x2) nogil
cpdef double gdtrib(double x0, double x1, double x2) nogil
cpdef double eval_hermite(long x0, double x1) nogil
cpdef double i0(double x0) nogil
cpdef double bdtrc(dl_number_t x0, dl_number_t x1, double x2) nogil
cpdef double ncfdtri(double x0, double x1, double x2, double x3) nogil
cpdef double i0e(double x0) nogil
cpdef double chdtri(double x0, double x1) nogil
cpdef double gdtrix(double x0, double x1, double x2) nogil
cpdef double chdtr(double x0, double x1) nogil
cdef void pro_rad1_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cpdef double nbdtrc(dl_number_t x0, dl_number_t x1, double x2) nogil
cpdef double nrdtrimn(double x0, double x1, double x2) nogil
cdef void pro_rad2_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cdef void pro_ang1(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cpdef double smirnovi(dl_number_t x0, double x1) nogil
cpdef double obl_cv(double x0, double x1, double x2) nogil
cdef void pro_rad1(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cpdef double huber(double x0, double x1) nogil
cpdef double chdtriv(double x0, double x1) nogil
cpdef double boxcox1p(double x0, double x1) nogil
cdef void airy(Dd_number_t x0, Dd_number_t *y0, Dd_number_t *y1, Dd_number_t *y2, Dd_number_t *y3) nogil
cpdef double exp2(double x0) nogil
cpdef double cosm1(double x0) nogil
cpdef double ncfdtrinc(double x0, double x1, double x2, double x3) nogil
cpdef double sindg(double x0) nogil
cpdef double nrdtrisd(double x0, double x1, double x2) nogil
cpdef Dd_number_t ndtr(Dd_number_t x0) nogil
cpdef double mathieu_b(double x0, double x1) nogil
cpdef double expn(dl_number_t x0, double x1) nogil
cpdef double zetac(double x0) nogil
cpdef Dd_number_t yv(double x0, Dd_number_t x1) nogil
cpdef Dd_number_t eval_laguerre(dl_number_t x0, Dd_number_t x1) nogil
cpdef double eval_hermitenorm(long x0, double x1) nogil
cpdef double pdtrik(double x0, double x1) nogil
cdef void mathieu_sem(double x0, double x1, double x2, double *y0, double *y1) nogil
cpdef double gammaincc(double x0, double x1) nogil
cpdef Dd_number_t jve(double x0, Dd_number_t x1) nogil
cdef void obl_ang1_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cpdef double boxcox(double x0, double x1) nogil
cpdef Dd_number_t log_ndtr(Dd_number_t x0) nogil
cpdef double nctdtrit(double x0, double x1, double x2) nogil
cdef void obl_ang1(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cpdef Dd_number_t eval_sh_jacobi(dl_number_t x0, double x1, double x2, Dd_number_t x3) nogil
cpdef double pdtr(dl_number_t x0, double x1) nogil
cpdef double nbdtr(dl_number_t x0, dl_number_t x1, double x2) nogil
cdef void hyp3f0(double x0, double x1, double x2, double x3, double *y0, double *y1) nogil
cdef void obl_rad2_cv(double x0, double x1, double x2, double x3, double x4, double *y0, double *y1) nogil
cpdef double chndtrix(double x0, double x1, double x2) nogil
cpdef double exprel(double x0) nogil
cpdef double ellipkm1(double x0) nogil
cpdef double y0(double x0) nogil
cpdef double nbdtri(dl_number_t x0, dl_number_t x1, double x2) nogil
cpdef Dd_number_t erfc(Dd_number_t x0) nogil
cpdef double kl_div(double x0, double x1) nogil
cpdef double struve(double x0, double x1) nogil
cpdef double gammaincinv(double x0, double x1) nogil
cpdef double btdtria(double x0, double x1, double x2) nogil
cdef void modfresnelm(double x0, double complex *y0, double complex *y1) nogil
cpdef double y1(double x0) nogil
cpdef double j1(double x0) nogil
cpdef double entr(double x0) nogil
cpdef double kolmogorov(double x0) nogil
cpdef double ncfdtridfn(double x0, double x1, double x2, double x3) nogil
cpdef double bei(double x0) nogil
cpdef double i1e(double x0) nogil
cpdef Dd_number_t hyp2f1(double x0, double x1, double x2, Dd_number_t x3) nogil
cpdef Dd_number_t expi(Dd_number_t x0) nogil
cpdef double gdtr(double x0, double x1, double x2) nogil
cpdef double inv_boxcox1p(double x0, double x1) nogil
cpdef double fdtridfd(double x0, double x1, double x2) nogil
cpdef double ndtri(double x0) nogil
cpdef double modstruve(double x0, double x1) nogil
cpdef Dd_number_t erf(Dd_number_t x0) nogil
cpdef double owens_t(double x0, double x1) nogil
cpdef double binom(double x0, double x1) nogil
cpdef double pro_cv(double x0, double x1, double x2) nogil
cpdef double complex hankel1e(double x0, double complex x1) nogil
cpdef double kerp(double x0) nogil
cdef void mathieu_modcem1(double x0, double x1, double x2, double *y0, double *y1) nogil
cdef void mathieu_cem(double x0, double x1, double x2, double *y0, double *y1) nogil
cpdef double cotdg(double x0) nogil
cpdef Dd_number_t dawsn(Dd_number_t x0) nogil
cpdef double smirnov(dl_number_t x0, double x1) nogil
cpdef Dd_number_t eval_chebys(dl_number_t x0, Dd_number_t x1) nogil
cpdef Dd_number_t log1p(Dd_number_t x0) nogil
cpdef double gammainccinv(double x0, double x1) nogil
cpdef double chndtridf(double x0, double x1, double x2) nogil
cpdef double j0(double x0) nogil
cpdef double ber(double x0) nogil
cdef void mathieu_modcem2(double x0, double x1, double x2, double *y0, double *y1) nogil