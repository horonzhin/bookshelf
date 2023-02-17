# -*- coding: utf-8 -*-
import datetime

from django import forms

from books.models import Author, Book, BookCategory, Cycle, Genre, Series


class AddBookForm(forms.ModelForm):
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 100, cur_year + 1)])

    cover = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    published = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Year', 'Month', 'Day')),
        required=False)
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    cycle = forms.ModelChoiceField(queryset=Cycle.objects.all(), required=False)
    new_cycle = forms.CharField(
        max_length=30, required=False, label='New cycle', widget=forms.TextInput(attrs={'class': 'form-control'}))
    series = forms.ModelChoiceField(queryset=Series.objects.all(), required=False)
    annotation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ModelChoiceField
    rating = forms.ModelChoiceField
    category = forms.ModelChoiceField(queryset=BookCategory.objects.all(), required=False)
    first_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Year', 'Month', 'Day')),
        required=False)
    second_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Year', 'Month', 'Day')),
        required=False)
    third_reading = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Year', 'Month', 'Day')),
        required=False)

    def __init__(self, *args, **kwargs):
        """Making the cycle field not required"""
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['cycle'].required = False

    def clean(self):
        """
        Clearing the "cycle" and "new cycle" fields.
        If both fields are empty, we give an error.
        If the only "cycle" field is empty, create a new "cycle" in the db with the name from the "new cycle" field.
        """
        cycle = self.cleaned_data.get('cycle')
        new_cycle = self.cleaned_data.get('new_cycle')
        if not cycle and not new_cycle:
            raise forms.ValidationError('You need to select a cycle from the list, or create a new cycle!')
        elif not cycle:
            cycle, created = Cycle.objects.get_or_create(name=new_cycle)
            self.cleaned_data['cycle'] = cycle

        return super(AddBookForm, self).clean()

    # todo = проверить логику создания нового цикла, если в списке нет нужного.
    # todo = создать такую же логику на series, author и genre

    class Meta:
        model = Book
        fields = '__all__'
