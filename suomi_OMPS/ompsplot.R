#this is a replacement script designed to provide point viewing similar to gooogle fusion tables.
#Thanks to Stamen Design for the tiles, and data by OpenStreetMap
library('plotly')
library(readr)
library(dplyr)
library(htmlwidgets)

args = commandArgs(trailingOnly=TRUE)

print("args are:")
print(args)

for (fname in args){
  points<-read_csv(fname)

  qttmp<-plot_ly(
    lon = points$lon,
    lat = points$lat,
    type = 'scattermapbox',
    marker = list(size = 7, color = 'orange'),
    mode="markers") %>%
      layout(
        hovermode='closest',
        mapbox = list(
          style = "stamen-terrain",
          zoom = 0),
        showlegend = T) 

  htmlwidgets::saveWidget(as_widget(qttmp), paste(tools::file_path_sans_ext(fname),"_view.html",sep='')) #create all htmlwidgets for easy selection and viewing
}



