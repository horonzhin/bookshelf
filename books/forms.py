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
    new_author = forms.CharField(
        max_length=30, required=False, label='New author', widget=forms.TextInput(attrs={'class': 'form-control'}))
    isbn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    published = forms.DateField(
        widget=forms.SelectDateWidget(years=year_range, empty_label=('Year', 'Month', 'Day')),
        required=False)
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    new_genre = forms.CharField(
        max_length=30, required=False, label='New genre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cycle = forms.ModelChoiceField(queryset=Cycle.objects.all(), required=False)
    new_cycle = forms.CharField(
        max_length=30, required=False, label='New cycle', widget=forms.TextInput(attrs={'class': 'form-control'}))
    series = forms.ModelChoiceField(queryset=Series.objects.all(), required=False)
    new_series = forms.CharField(
        max_length=30, required=False, label='New series', widget=forms.TextInput(attrs={'class': 'form-control'}))
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
        """Making fields not required"""
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['cycle'].required = False
        self.fields['series'].required = False
        self.fields['genre'].required = False
        self.fields['author'].required = False

    def clean(self):
        """
        A method for clearing the specified fields and
        writing new data if the necessary ones are not among those recorded earlier.
        """
        # clearing the "cycle" and "new_cycle" fields
        cycle = self.cleaned_data.get('cycle')
        new_cycle = self.cleaned_data.get('new_cycle')
        # if the existing cycles do not have the necessary and indicate a new in the "new_cycle" field, then create it
        if new_cycle and not cycle:
            cycle, created = Cycle.objects.get_or_create(name=new_cycle)
            self.cleaned_data['cycle'] = cycle

        # clearing the "series" and "new_series" fields
        series = self.cleaned_data.get('series')
        new_series = self.cleaned_data.get('new_series')
        # if the existing series do not have the necessary and indicate a new in the "new_series" field, then create it
        if new_series and not series:
            series, created = Series.objects.get_or_create(name=new_series)
            self.cleaned_data['series'] = series

        genre = self.cleaned_data.get('genre')
        new_genre = self.cleaned_data.get('new_genre')
        # If both fields are empty, we give an error
        if not genre and not new_genre:
            raise forms.ValidationError('You need to select a genre from the list, or create a new genre!')
        else:
            genre, created = Genre.objects.get_or_create(name=new_genre)
            self.cleaned_data['genre'] = [genre]

        author = self.cleaned_data.get('author')
        new_author = self.cleaned_data.get('new_author')
        # If both fields are empty, we give an error
        if not author and not new_author:
            raise forms.ValidationError('You need to select a author from the list, or create a new author!')
        # If the only "author" field is empty, create a new "author" in the db with the name from the "new_author" field
        elif not author:
            first_name, last_name = new_author.split()
            author, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
            self.cleaned_data['author'] = [author]

        return super(AddBookForm, self).clean()

    class Meta:
        model = Book
        # If specify __all__ because of the required user field,
        # it will not be possible to override the form_valid() method in AddBookView
        fields = [
            'cover', 'title', 'author', 'new_author', 'isbn', 'published', 'genre', 'new_genre', 'cycle', 'new_cycle',
            'series', 'new_series', 'annotation', 'status', 'rating', 'category', 'first_reading', 'second_reading',
            'third_reading'
        ]
