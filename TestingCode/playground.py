

def x(meters, current_distance):

    previous_distance = meters // 10
    
    if previous_distance and previous_distance != current_distance:
        current_distance = previous_distance
        return current_distance
    else:
        return None

def main():
    current_distance = 0

    ret = x(10, current_distance)
    current_distance = ret
    ret = x(10, current_distance)
    current_distance = ret
    print(ret)
    

if __name__ == '__main__':
    main()