path = "C:/Users/Daniel/Dropbox/GitHub/Washboards-Simulation/csv"
setwd(path)

files <- list.files(path)
show(files)

#road.x | road.f
road <- read.csv(files[1])
colnames(road) <- c("x", "f")
x_max = max(road$x)

#sinus profile
 # x_max = 10*4
 # x_step = 0.05
 # x_sin = seq(0,x_max, x_step)
 # y_sin = sin(2*pi*x_sin)
 # sin_data = data.frame(x= x_sin, f = y_sin)

data = road
data$f = data$f - mean(data$f)


#Plotting parameters
  lwd = 2
  asp_ratio = 1
  lag_max = x_max
  par(mfrow = c(1,2))
  
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



lags = seq(0, x_max+1, 1)
lags = seq(-(x_max+1)/2, (x_max+1)/2, 1)

acfs = numeric(length(lags))
i=1
for(lambda in lags){
  acfs[i] = acf_disc(data$f, 0:(length(data$x)-1), 
                     lambda, length(data$x) )
  i=i+1
}

par(mfrow = c(1,1))
maxima = lags[which(diff(sign(diff(acfs)))==-2)]+1

ini = 0#150
fin = 500#115
plot(road$x[ini:fin], road$f[ini:fin], type = 'l', asp = asp_ratio,
     lwd = lwd)
abline(v = seq(0,fin, (maxima[2]-maxima[1]+1)  ) )

plot(lags, acfs, type = 'l')
abline(v = maxima)

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