def hanging_line(point1, point2):
    # CODE FROM:
    # https://stackoverflow.com/questions/30008322/draw-a-curve-connecting-two-points-instead-of-a-straight-line
    a = (point2[1] - point1[1])/(np.cosh(point2[0]) - np.cosh(point1[0]))
    b = point1[1] - a*np.cosh(point1[0])
    x = np.linspace(point1[0], point2[0], 100)
    y = a*np.cosh(x) + b

    return (x,y)

def plotSankey(df1, df2, key, ct):
    # Combine the dataframes on an outer join
    df = df1.merge(df2, on=key, how='outer', suffixes=('.1', '.2'))
    
    # Replace all nan with 0
    df = df.fillna(0)
    
    
    # Generate y values for start
    ct1 = '{}.1'.format(ct)
    ct2 = '{}.2'.format(ct)
    iterValues = ((ct1, ct2, key), (ct2, ct1, key))
    
    
    for c,i in enumerate(iterValues):
        df = df.sort_values(by=list(i), ascending=[False, False, True])
        yTotal = df[i[0]].sum()

        counter = yTotal
        yStart,yEnd = [],[]
        for item in list(df[i[0]]):
            yStart.append(counter)
            yEnd.append(counter - item)
            counter = counter - item
        # Add values
        df['y.{}.start'.format(c+1)] = yStart
        df['y.{}.end'.format(c+1)] = yEnd
    
    
    fig,ax = plt.subplots(1, 1, figsize=(10,20))
    
    for i in df.iterrows():
        row = i[1]
        
        y = []
        for j in ['start', 'end']:  
            coord = []
            for xx,k in enumerate([1, 2]):
                coord.append([xx, row['y.{}.{}'.format(k, j)]])
            
            res = hanging_line(*coord)
            x = res[0]
            y.append(res[1])
            
            
        #print(y)
        ax.fill_between(x, y[0], y[1])
            
        
    
    
    plt.show()
    return df
    
    
#     y1TotalSize,y2TotalSize = np.sum(s1),np.sum(s2)
    
#     # Establish starting locations for y1
#     print(y1TotalSize,y2TotalSize)