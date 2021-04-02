function compareBodies(a,b) {
    mistakes = 0
    for (i in length(a)) {
    mistakes += (a[i] - b[i])*(a[i] - b[i])    
    }
    mistakes = Math.sqrt(mistakes)
}