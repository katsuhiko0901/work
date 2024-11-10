from django import forms 

# パスをテキスト入力させるのは何か違う氣がする…
class PathForm(forms.Form):
    PathForm = forms.CharField(required=True,label='image_path',max_length=255,strip=True,)

# 画像をアップロードしてそのパスを指定するように変更
class UploadFileForm(forms.Form):
    file = forms.ImageField()

