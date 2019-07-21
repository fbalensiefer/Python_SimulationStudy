# -*- coding: utf-8 -*-
###############################################################################
#       Preface
###############################################################################

rm(list=ls())
#setwd('/Users/Fabian/Google Drive/UniBonn/X_Microeconometrics/student-project-fbalensiefer')
setwd('C:/Users/fabia/Google Drive/UniBonn/X_Microeconometrics/student-project-fbalensiefer')


# preface loading packages required for R
library(plm)
library(lfe)
#library(haven)
library(dplyr)
library(dummies)
library(data.table)
#library(fastDummies)

###############################################################################
#       Two-way FE function
###############################################################################
TwoWayFE <- function(y, Xs, fe1, fe2, dt, cluster = FALSE) {
  pkgs <- c("data.table", "RcppEigen")
  sapply(pkgs, require, character.only = TRUE)
  
  keep_cols <- c(y, Xs, fe1, fe2)
  model_dt <- dt[, keep_cols, with = FALSE]; rm(keep_cols)
  model_dt <- na.omit(model_dt)
  
  num_Xs <- length(Xs)
  new_names <- c("y", paste0("x", 1:num_Xs), "fe1", "fe2")
  setnames(model_dt, 1:ncol(model_dt), new_names)
  
  # Sample Means:
  cols <- new_names[!grepl("fe", new_names)]
  model_dt[, paste0("mean_", cols) :=
             lapply(.SD, mean, na.rm = TRUE), .SDcols = cols]
  
  # Means by FE1:
  setkey(model_dt, fe1)
  model_dt[,
           paste0("mean_", cols, "_fe1") :=
             lapply(.SD, mean, na.rm = TRUE), .SDcols = cols, by = fe1]
  M <- length(unique(model_dt$fe1))
  
  # Means by FE2:
  setkey(model_dt, fe2)
  model_dt[,
           paste0("mean_", cols, "_fe2") :=
             lapply(.SD, mean, na.rm = TRUE), .SDcols = cols, by = fe2]
  Y <- length(unique(model_dt$fe2))
  
  # Demeaning:
  model_dt[, "y_tilde" := y - mean_y_fe2 - mean_y_fe1 + mean_y]
  
  g <- function(i) {paste0("x",i,"_tilde")}
  LHS <- sapply(1:num_Xs, g)
  
  f <- function(i) {
    paste0("x",i," - mean_x",i,"_fe2 - mean_x",i,"_fe1 + mean_x", i)
  }
  RHS <- paste0("list(",paste(sapply(1:num_Xs, f), collapse = ", "), ")")
  
  model_dt[, eval(LHS) := eval(parse(text = RHS))]
  
  x_cols <- grep("x\\d{1}_tilde", names(model_dt), value = TRUE)
  model_dt <- model_dt[, c("y_tilde", eval(x_cols), "fe1", "fe2"),
                       with = FALSE]
  
  y <- model_dt$y_tilde
  X <- model_dt[, x_cols, with = FALSE]
  cluster_vec <- model_dt$fe1
  rm(model_dt)
  
  m <- RcppEigen::fastLm(X, y)
  names(m$coefficients) <- Xs
  
  ##############################################
  DoF <- m$df.residual - (M - 1) - (Y - 1) - num_Xs + 1
  # No intercept in model.
  
  # SEs:
  if(cluster){
    N <- length(cluster_vec)
    K <- m$rank + (M - 1) + (Y - 1)  + 1
    
    dfc <- (M/(M - 1)) * ((N - 1)/(N - K))
    est_fun <- residuals(m) * X
    
    dt <- data.table(est_fun, fe1 = cluster_vec)
    
    setkey(dt, fe1)
    dt <- dt[, lapply(.SD, sum), by = fe1][, 2:ncol(dt), with = FALSE]
    
    bread <- solve(crossprod(as.matrix(X))) * N
    meat <- crossprod(as.matrix(dt)) / N
    
    m$se <- as.numeric(sqrt(dfc * 1/N * diag(bread %*% meat %*% bread)))
    message("SEs Clustered on First FE")
  } else {
    m$se <- m$se * sqrt(m$df.residual / DoF)
    message("SEs Not Clustered")
  }
  
  # Correcting degrees of freedom:
  m$df.residual <- DoF
  
  return(m)
}

###############################################################################
###         Main Results
###############################################################################

# Table 6: First-Stage and Reduced-Form estimates
df = read.csv("test_csv.csv")
df = distinct(df)
#test=dummy_cols(df, select_columns = c('indivID','group_timeID'))
temp=colnames(df)
#dt=as.data.table(df)
temp=temp[46:174]
vars=paste(temp, collapse='+')
dep='num_closings ~ '
model= paste(dep, vars, collapse='')
fixeff='+as.factor(indivID)+as.factor(group_timeID)'
femodel='| indivID + group_timeID'
model2=paste(model, fixeff, collapse='')
model3=paste(model, femodel, collapse='')
#reg = TwoWayFE(y='num_closings', Xs=temp, fe1='indivID', fe2='group_timeID', dt=dt, cluster=FALSE)
#reg=felm(formula=model3, data=df)
reg=plm(model, df, index=c('indivID','group_timeID'), model='within', effect='twoways')
#reg=lm(model2, df)
summary(reg)

# simulation sample
panel_sample <- read.csv("C:/Users/fabia/Google Drive/UniBonn/X_Microeconometrics/student-project-fbalensiefer/panel_sample.csv")
panel_sample['DD']=panel_sample$M*panel_sample$Exp
model='Y ~ DD + c(indivID) + c(group_timeID)'
reg=lm(model,panel_sample)
summary(reg)
femod=felm(Y ~ DD | indivID + group_timeID, data=panel_sample)
summary(femod)
