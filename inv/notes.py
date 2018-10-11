#                    sum_plus = RegDeviceStock.objects.filter(operation_type='+', device=rec.device).values('device').annotate(qty_sum=Sum('qty'))
#                    sum_minus = RegDeviceStock.objects.filter(operation_type='-', device=rec.device).values('device').annotate(qty_sum=Sum('qty'))
#                    if sum_plus:
#                        sum_plus = sum_plus[0]['qty_sum']
#                    else:
#                        sum_plus = 0
#                    if sum_minus:
#                        sum_minus = sum_minus[0]['qty_sum']
#                    else:
#                        sum_minus = 0
