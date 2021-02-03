# Các thư viện cần thiết
import requests
from bs4 import BeautifulSoup
import re



# Hàm tìm kiếm các URL liên quan để tải xuống
# Truyền vào URL cần được quét, và URL xuất phát
def tim_url_lien_quan(url, url_chinh):
    url_tim_duoc = set()
    link = requests.get(url)
    link_soup = BeautifulSoup(link.text, 'html.parser')
    results = link_soup('a', attrs={'href': True})
    for i in results:
        a = i['href']
        mau = f'^{url_chinh}[^?#]*$'
        mau2 = '^/[^?#]*$'
        if re.match(mau, a):
            url_tim_duoc.add(a)
        else:
            if re.match(mau2, a):
                url_lien_quan = f'{url_chinh}{a}'
                url_tim_duoc.add(url_lien_quan)
    return url_tim_duoc


# Tăng số lượng URL
# Truyền vào các phần tử cần được duyệt và URL xuất phát
# Trả về tập hợp các URL
def them_va_duyet_hang_cho(hang_cho, url_chinh, so_luong_trang):
    history = hang_cho
    while (len(hang_cho) > 0) and (len(history) < so_luong_trang):
        url_tim_duoc = tim_url_lien_quan(hang_cho.pop(), url_chinh)
        hang_cho = hang_cho | (url_tim_duoc - history)
        history = history | url_tim_duoc
    return history


def main():
    url_tim_duoc = tim_url_lien_quan('https://vietnamnet.vn', 'https://vietnamnet.vn')
    history = them_va_duyet_hang_cho(url_tim_duoc)
    for i in history:
        print(i)


if __name__ == '__main__':
    main()