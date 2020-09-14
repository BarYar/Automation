def roman():
    romdic={"I":1,"V":5,"X":10,"L":50,"C":100}
    SC={"IV":4,"IX":9}
    stspe=""
    st=""
    loc=""
    num=int(input("Enter your number"))
    if(num>0):
        cnum=int(num)
        difm=num
        if(cnum%10==4):
            stspe="IV"
            cnum=cnum-4
            num=cnum
        if (cnum % 10 == 9):
            stspe="IX"
            cnum = cnum - 9
            num = cnum
        while(cnum>0):
            for i in romdic:
                difn=cnum-romdic[i]
                if(difn<0):
                    break
                if(difn<difm):
                    difm=difn
                    loc=i
            cnum=difm
            st=st+loc
            difm=cnum
        st=st+stspe
        print(st)
roman()


