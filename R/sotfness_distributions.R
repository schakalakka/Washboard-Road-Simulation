#
dev.off()
par(mfrow = c(1,1))

standard_height = 10

f <- function(h,h0 = standard_height){
  a = 3/h0^2*(1-2/h0)
  b = 6/h0^2*(1-h0/3)
  return(a*h^2+b*h)
}

x = seq(0,standard_height, by = 0.1)
plot(x, f(x))
abline(h = 0)

f <- function(h, h0 = standard_height){
  a = 3/h0^3
  return(a*h^2)
}

x = seq(0,standard_height, by = 0.1)
plot(x, f(x))
abline(h = 0)

int_f <- function(h, h0 = standard_height){
  return(h^3/h0^3)
}

x = seq(0,standard_height, by = 0.1)
plot(x, int_f(x))
print(int_f(0:standard_height))
abline(h=0.5)


f2 <- function(h, h0 = standard_height, alpha = 1){
  A = alpha/(exp(alpha*h0)-1)
  return(A*exp(alpha*h))
}

int_f2 <- function(h, h0 = standard_height, alpha = 1){
  return( (exp(alpha*h)-1)/(exp(alpha*h0)-1) )
}

h0 = 10
alpha = 0.5

x = seq(0,h0, by = 0.1)
plot(x, int_f2(x,h0,alpha))
print(int_f2(0:h0, h0, alpha))
abline(h=0.5)


################
################
f3 <- function(h, h0 = standard_height, alpha = 1){
  A = alpha/(exp(alpha*h0))
  return(A*exp(alpha*h))
}

int_f3 <- function(h, h0 = standard_height, alpha = 1){
  return( exp(alpha*(h-h0)) )
}

#h0 = 5
#alpha = 0.3

h0 = 10
alphas = c(1,0.5, 0.2, 0.1, 0.01)
colors = c("black", "blue", "green", "orange", "red")
x = seq(0,h0, by = 0.05)
plot(x, int_f3(x,h0,alphas[1]), type = 'l', lwd = 2,
     ylab = 'Probability',
     xlab = 'Height (block units)',
     cex.lab =1.25)
for(i in 2:(length(alphas))){
  lines(x, int_f3(x,h0,alphas[i]), lwd = 2, col = colors[i])
}


legend("topleft", 
       paste("alpha =", as.character(alphas)), 
       col = colors,lwd=2, bty ='n', 
       cex = 0.8, 
       seg.len = 0.5)


print(int_f3(0:h0, h0, alpha))
abline(h=0.5, lty = 2)






