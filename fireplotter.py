import get_from_fire as getdata
import datetime
from pprint import pprint
import io
import base64
import matplotlib.pyplot as plt

def return_plot():
    fp_ids_of_psdlk = [171258213, 135499785, 61178981, 215950478, 154100195]
    fp_names_of_psdlk = ['DavMan', 'Dell', 'NaniS', 'wocetake', 'Got the Life']
    daily_stats_collection = getdata.get_daily_stats_collection()
    final_table = [['Date', 'DavMan', 'Dell', 'NaniS', 'wocetake', 'Got the Life']]

    for doc in daily_stats_collection:
        l_one = str(doc.id)
        l_two = doc.to_dict()['DavMan']
        l_three = doc.to_dict()['Dell']
        l_four = doc.to_dict()['NaniS']
        l_five = doc.to_dict()['wocetake']
        l_six = doc.to_dict()['Got the life']
        temp_list = (l_one, l_two, l_three, l_four, l_five, l_six)
        final_table.append(temp_list)
    dav_total = dell_total = nanis_total = wocetake_total = gtl_total = 0

    for item in final_table:
        if item[0] != 'Date':
            dav_total += item[1]
            dell_total += item[2]
            nanis_total += item[3]
            wocetake_total += item[4]
            gtl_total += item[5]

    fin_arr = [dav_total, dell_total, nanis_total, wocetake_total, gtl_total]
    plt.bar(fp_names_of_psdlk, fin_arr)
    plt.title('Top Spammer EU - Last Week')
    plt.ylabel('Messages')

    #now we turn the plot into an image to pass to main
    plot_img = plt.gcf()
    buf = io.BytesIO()
    plot_img.savefig(buf, format='png')
    buf.seek(0)
    string_of_plot_image = base64.b64encode(buf.read())

    #generate text msg based on fin_arr
    who_index = fin_arr.index(max(fin_arr))
    who = fp_names_of_psdlk[who_index]
    share_spam = round(fin_arr[who_index]*100/sum(fin_arr),2)
    weekly_stats_string = 'Spammer of the week: *' + str(who) + '*!\n' + str(max(fin_arr)) + ' messages, ' + str(share_spam) + '%' + ' of total! Together we sent ' + str(sum(fin_arr)) + ' messages.'

    #return string + img
    return weekly_stats_string, string_of_plot_image

return_plot()
