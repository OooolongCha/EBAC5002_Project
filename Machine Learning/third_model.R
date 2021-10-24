#install.packages("rattle")
#install.packages("rpart.plot")
#install.packages("ROCR")
#install.packages("ggplot2")

library(rpart)


dataset <- read.csv("youtubedetail.csv",header=TRUE)
#dataset <- read.csv("~/telcochurn.csv",header=TRUE)
dataset$high_comment<-as.factor(dataset$high_comment)
dataset$high_view<-as.factor(dataset$high_view)

set.seed(seed) 
nobs <- nrow(dataset)  
trainData <- sample(nrow(dataset), 0.5*nobs) 

testData <- setdiff(seq_len(nrow(dataset)), trainData) 

# Build the Decision Tree model.

input <- 2:3       #views	comment_count

target<- 8   #high_like

input2<- 9:10

library(randomForest)
set.seed(6666)
rf <- randomForest(as.factor(high_like) ~ ., data=dataset[trainData,c(input, target)],importance=TRUE,na.action = na.pass)
print(rf)

plot(rf,main = "Random forest prediction error rate")
importance(rf)
varImpPlot(rf)
#predict in testdata
set.seed(666)
rf.test<-predict(rf,newdata = dataset[testData,c(input, target)])
rf.cf<- caret::confusionMatrix(as.factor(rf.test),as.factor(dataset[testData,c(input, target)]$high_like))
rf.cf

rf.test2<-predict(rf,newdata=dataset[testData,c(input, target)],type = "prob")

library(pROC)
roc.rf<-multiclass.roc(dataset[testData,c(input, target)]$high_like, rf.test2)
roc.rf




















