echo "make1d.py Runtime:"
echo "$(time ( ./make1d.py ) 2>&1 1>/dev/null )"
echo
echo "c2f.py Runtime:"
echo "$(time ( ./c2f.py ) 2>&1 1>/dev/null )"
echo
echo "runlsqr.py Runtime:"
echo "$(time ( ./runlsqr.py ) 2>&1 1>/dev/null )"



# make1dtime="$(time ( ./make1d.py ) 2>&1 1>/dev/null )"
# c2ftime="$(time ( ./c2f.py ) 2>&1 1>/dev/null )"
# runlsqrtime="$(time ( ./runlsqr.py ) 2>&1 1>/dev/null )"
# 
# 
# echo "$make1dtime"
# echo "$c2ftime"
# echo "$runlsqrtime"