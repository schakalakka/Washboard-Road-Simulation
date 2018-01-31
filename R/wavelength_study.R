
library(Hmisc)

path = "C:/Users/Daniel/Dropbox/GitHub/Washboards-Simulation/csv"
setwd(path)

files <- list.files(path)
show(files)

#road.x | road.f
filenum = 11
road <- read.csv(files[filenum])

colnames(road) <- c("x", "f")
x_max = max(road$x)

#sinus profile
 # x_max = 10*4
 # x_step = 0.05
 # x_sin = seq(0,x_max, x_step)
 # y_sin = sin(2*pi*x_sin)
 # sin_data = data.frame(x= x_sin, f = y_sin)

  # x_sin = seq(0,x_max, 1)
  # y_sin = 10*cos((2*pi)/(60)*x_sin)+100
  # sin_data = data.frame(x= x_sin, f = y_sin)
  #plot(sin_data$x, sin_data$f, type = 'l', asp = asp_ratio)

data = road
data$f = data$f - mean(data$f)


#Plotting parameters
  lwd = 2
  asp_ratio = 1
  lag_max = x_max
  par(mfrow = c(1,2))
  cex.lab = 1.25
  cex.main = 1.25
  
  
# #Plot road's surface
#   plot(data, type = 'l', asp = asp_ratio,
#        lwd = lwd)
# 
# #Plot autocorrelation function
#   acf(data$f, lag = lag_max)
# 
# #Plot periodogram
#   a <- spectrum(data$f, log = "no")
#   plot((2*a$freq)^(-1),a$spec)
#   #a$freq = log(a$freq)
#   a$spec = log(a$spec)
#   plot(a$freq,a$spec)

#ACF discrete

u_xl <- function(u,x, l, period){
    x <- (x+l) %% period
    return(u[x+1]) #+1 because in R indices start with 1 not 0
  }
  
acf_disc <- function(ts = road$f, x =road$x, 
                     lag = 0, 
                     period = dim(road)[1]){
  u_x = ts
  num = 0
  denom = 0
  u_xl = u_xl(u_x, x,lag, period)
  num = sum(u_x*u_xl)   
  denom = sum(u_x^2)
  acf_lag = num/denom
  return(acf_lag)
}


acf_disc(data$f, 0:(length(data$x)-1), 0, length(data$x) )

###############################################
#Plotting road's surface and autocorrelation
################################################
#######
# Initial road profile
############


road <- read.csv(files[filenum+1])

colnames(road) <- c("x", "f")
x_max = max(road$x)

data = road
data$f = data$f - mean(data$f)

par(mfrow = c(2,2))
maxima = lags[which(diff(sign(diff(acfs)))==-2)]

ini = 0#150
fin = 500#115
x = road$x[ini:fin]
y = road$f[ini:fin]
plot(x, y, type = 'l', asp = 10,
     lwd = lwd,
     ylab = "",
     main = expression("Initial road surface, " ~ alpha ~ "=0.1" ),
     xlab = "Horizontal position, x (block size units)",
     cex.lab = cex.lab,
     cex.main = cex.main
)
title(ylab = "Initial f(x) (block size units)", line = 2,
      cex.lab = cex.lab)
#abline(v = seq(0,fin, (maxima[2]-maxima[1]-2)  ), lty = 2)
abline(h = 0)
polygon(c(0, 1:fin,fin), c(90, road$f*1  ,90), col=gray(0.95), border=NA)

#minor.tick(nx=2, ny=10, tick.ratio=0.5)







lags = seq(0, x_max+1, 1)
#lags = seq(-(x_max+1)/2, (x_max+1)/2, 1)

acfs = numeric(length(lags))
i=1
for(lambda in lags){
  acfs[i] = acf_disc(data$f, 0:(length(data$x)-1), 
                     lambda, length(data$x) )
  i=i+1
}

#dev.off()

plot(lags, acfs, type = 'l', lwd = lwd,
     main = expression("Initial autocorrelation function"),
     ylab = "",
     xlab = "Lag, k (block size units)",
     cex.lab = cex.lab,
     cex.main = cex.main
)
title(ylab = expression('R'[f]('k')  ~" (ACF)"),line = 2,
      cex.lab = cex.lab)

#abline(v = maxima, lty = 2)
#minor.tick(nx=2, ny=5, tick.ratio=0.5)



####################
#FINAL SURFACE
###############
road <- read.csv(files[filenum])

colnames(road) <- c("x", "f")
x_max = max(road$x)
data = road
data$f = data$f - mean(data$f)


lags = seq(0, x_max+1, 1)
#lags = seq(-(x_max+1)/2, (x_max+1)/2, 1)

acfs = numeric(length(lags))
i=1
for(lambda in lags){
  acfs[i] = acf_disc(data$f, 0:(length(data$x)-1), 
                     lambda, length(data$x) )
  i=i+1
}

#dev.off()
#par(mfrow = c(1,2))

maxima = lags[which(diff(sign(diff(acfs)))==-2)]
if(files[filenum]=="attempt-4_after.csv"){
  maxima = c( 36,  74, 107,  143, 188, 222, 276, 310,
              355,  391, 424,              462)
  }
if( files[filenum]=="attempt-5_after.csv" ){
  maxima = c(  37, 73, 107, 141, 179, 211, 249, 287, 
               319, 357, 391, 427, 461)
}

if( files[filenum]=="attempt-3_after.csv" ){
  maxima = c(  47, 100,  149, 202, 249, 296, 349, 398, 451)
}

ini = 0#150
fin = 500#115
x = road$x[ini:fin]
y = road$f[ini:fin]
plot(x, y , type = 'l', asp = asp_ratio,
     lwd = lwd,
     ylab = "",
     main = expression("Final road surface, " ~ alpha ~ "=0.1" ),
     xlab = "Horizontal position, x (block size units)",
      cex.lab = cex.lab,
      cex.main = cex.main
     )
title(ylab = "Final f(x) (block size units)", line = 2,
      cex.lab = cex.lab)
abline(v = seq(0,fin, (maxima[2]-maxima[1]-2)  ), lty = 2)
abline(h = 0)
polygon(c(0, 1:fin,fin), c(0, road$f*0.98  ,0), col=gray(0.95), border=NA)

#minor.tick(nx=2, ny=10, tick.ratio=0.5)


#polygon(c(0, 1:fin,fin), c(-400, x*0  ,-400), col=gray(0.1), border=NA)

# plot(range(x), c(0, max(y)), type='n', xlab="X", ylab="Y")
# 
# polygon(c(0, 1:500,500), c(20, road$f  ,20), col=1, border=NA)

plot(lags, acfs, type = 'l', lwd = lwd,
     main = expression("Final autocorrelation function"),
     ylab = "",
     xlab = "Lag, k (block size units)",
      cex.lab = cex.lab,
      cex.main = cex.main
     )
title(ylab = expression('R'[f]('k')  ~" (ACF)"),line = 2,
      cex.lab = cex.lab)

abline(v = maxima, lty = 2)
#minor.tick(nx=2, ny=5, tick.ratio=0.5)
####################################################################
#####################################################################

average_wavelength <- function(maxima){
  sum=0
  counter = 0
  for(i in 1:(length(maxima)-1) ){
    sum = maxima[i+1]-maxima[i]
    counter = counter+1
  }
  return(sum/counter)
}

wavelength = average_wavelength(maxima)
show(maxima)

############################################################
#Plot sinus 
############################################################

# #sinus profile
# #x_max = 10*4
# #x_step = 0.05
# x_sin = seq(0,x_max, 1)
# y_sin = 0.2*sin((2*pi)/(60)*x_sin)
# sin_data = data.frame(x= x_sin, f = y_sin)
# plot(sin_data$x, sin_data$f, type = 'l', asp = asp_ratio)


#par(mfrow = c(1,2))




x_sin = seq(0,x_max, 1)
lambda = 60
y_sin = 10*cos((2*pi)/(lambda)*x_sin)+100
sin_data = data.frame(x= x_sin, f = y_sin)
data = sin_data
data$f = data$f - mean(data$f)

ini = 0#150
fin = length(data$x)#115
x = data$x[ini:fin]
y = sin_data$f[ini:fin]

lags = seq(0, x_max+1, 1)
#lags = seq(-(x_max+1)/2, (x_max+1)/2, 1)

acfs = numeric(length(lags))
i=1
for(lambda in lags){
  acfs[i] = acf_disc(data$f, 0:(length(data$x)-1), 
                     lambda, length(data$x) )
  i=i+1
}
maxima = lags[which(diff(sign(diff(acfs)))==-2)]+1


plot(x, y , type = 'l', asp = asp_ratio,
     lwd = lwd,
     ylab = "",
     main = expression("Sinusoidal surface, " ~ lambda ~ "=60" ),
     xlab = "Horizontal position, x (block size units)",
     cex.lab = cex.lab,
     cex.main = cex.main
)
title(ylab = expression("g(x)="  ~10 ~ cos(2*pi~'/' ~lambda~ 'x')~'+100'~" (block size units)"), line = 2,
      cex.lab = cex.lab)
abline(v = seq(0,fin, (maxima[2]-maxima[1])  ), lty = 2)
abline(h = 0)
polygon(c(0, 1:fin,fin), c(0, sin_data$f*0.98  ,0), col=gray(0.95), border=NA)

minor.tick(nx=2, ny=10, tick.ratio=0.5)


#polygon(c(0, 1:fin,fin), c(-400, x*0  ,-400), col=gray(0.1), border=NA)

# plot(range(x), c(0, max(y)), type='n', xlab="X", ylab="Y")
# 
# polygon(c(0, 1:500,500), c(20, road$f  ,20), col=1, border=NA)




plot(lags, acfs, type = 'l', lwd = lwd,
     main = expression("Autocorrelation function"),
     ylab = "",
     xlab = "Lag, k (block size units)",
     cex.lab = cex.lab,
     cex.main = cex.main
)
title(ylab = expression('R'[g]('k')  ~" (ACF)"),line = 2,
      cex.lab = cex.lab)

abline(v = maxima, lty = 2)
minor.tick(nx=2, ny=5, tick.ratio=0.5)

###########################################################
############################################################

