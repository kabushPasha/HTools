::net use Z: \\diskstation\Fileserver\Projects canoecanoe /user:guest /persistent:yes
cmdkey /add:diskstation /user:diskstation\guest /pass:canoecanoe
net use Z: \\diskstation\Fileserver\Projects /persistent:yes
pause