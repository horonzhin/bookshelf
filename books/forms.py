# -*- coding: utf-8 -*-
import datetime

from django import forms

from books.models import Book, Author, Genre, Cycle, Series, BookCategory


class AddBookForm(forms.ModelForm):
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 100, cur_year + 1)])

    cover = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    published = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Год', 'Месяц', 'День')),
        required=False)
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    cycle = forms.ModelChoiceField(queryset=Cycle.objects.all(), required=False)
    new_cycle = forms.CharField(
        max_length=30, required=False, label='Новый цикл', widget=forms.TextInput(attrs={'class': 'form-control'}))
    series = forms.ModelChoiceField(queryset=Series.objects.all(), required=False)
    annotation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField
    rating = forms.ModelChoiceField
    category = forms.ModelChoiceField(queryset=BookCategory.objects.all(), required=False)
    first_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Год', 'Месяц', 'День')),
        required=False)
    second_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Год', 'Месяц', 'День')),
        required=False)
    third_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Год', 'Месяц', 'День')),
        required=False)

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        # make `cycle` not required, we'll check for one of `cycle` or `new_cycle` in the `clean` method
        self.fields['cycle'].required = False

    def clean(self):
        cycle = self.cleaned_data.get('cycle')
        new_cycle = self.cleaned_data.get('new_cycle')
        if not cycle and not new_cycle:
            # neither was specified so raise an error to user
            raise forms.ValidationError('Необходимо указать цикл из списка, либо создать новый цикл!')
        elif not cycle:
            # get/create `cycle` from `new_cycle` and use it for `cycle` field
            cycle, created = Cycle.objects.get_or_create(name=new_cycle)
            self.cleaned_data['cycle'] = cycle

        return super(AddBookForm, self).clean()

    # todo = проверить логику создания нового цикла, если в списке нет нужного.
    # todo = создать такую же логику на series, author и genre

    class Meta:
        model = Book
        fields = '__all__'
