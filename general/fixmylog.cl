files *.fit > images.list
hselect images=@images.list fields=$I,EXPTIME,FILTER,AIRMASS,UTC,INSTFOCU expr=yes > images_info.list
!echo "I\tEXPTIME\tFILTER\tAIRMASS\tUTC\tINSTFOCU" > header
!cat header images_info.list > concat.tmp
!cat concat.tmp > images_info.list
!rm -rf ./header
!rm -rf ./concat.tmp
