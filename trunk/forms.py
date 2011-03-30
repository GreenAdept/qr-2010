from django import forms

# Create the form class.
class UserRegistrationForm(forms.Form):
        usern = forms.CharField(max_length=30, required = True)
        passw = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=50, required = True)
        passwr = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=50, required = True)
        uemail = forms.EmailField(required = True)
        firstname = forms.CharField(max_length=50, required = True)
        lastname = forms.CharField(max_length=50, required = True)
        photo = forms.ImageField(required=False,widget = forms.FileInput(attrs={'class':'fileChooser'}))
        gender = forms.ChoiceField(widget = forms.Select(), choices = ([('','Select'), ('Male','Male'), ('Female','Female'), ]), required = False,)
        day = forms.ChoiceField(widget = forms.Select(), choices = ([('','Day'),
                                          ('1','1'),
                                          ('2','2'),
                                          ('3','3'),
                                          ('4','4'),
                                          ('5','5'),
                                          ('6','6'),
                                          ('7','7'),
                                          ('8','8'),
                                          ('9','9'),
                                          ('10','10'),
                                          ('11','11'),
                                          ('12','12'),
                                          ('13','13'),
                                          ('14','14'),
                                          ('15','15'),
                                          ('16','16'),
                                          ('17','17'),
                                          ('18','18'),
                                          ('19','19'),
                                          ('20','20'),
                                          ('21','21'),
                                          ('22','22'),
                                          ('23','23'),
                                          ('24','24'),
                                          ('25','25'),
                                          ('26','26'),
                                          ('27','27'),
                                          ('28','28'),
                                          ('29','29'),
                                          ('30','30'),
                                          ('31','31'),]), required = False,)
        month = forms.ChoiceField(widget = forms.Select(), choices = ([('','Month'),
                                                                       ('1','January'),
                                                                       ('2','February'),
                                                                       ('3','March'),
                                                                       ('4','April'),
                                                                       ('5','May'),
                                                                       ('6','June'),
                                                                       ('7','July'),
                                                                       ('8','August'),
                                                                       ('9','September'),
                                                                       ('10','October'),
                                                                       ('11','November'),
                                                                       ('12','December'), ]), required = False,)
        year = forms.ChoiceField(widget = forms.Select(), choices = ([('','Year'),
                                                                       ('2010','2010'),
                                                                       ('2009','2009'),
                                                                       ('2008','2008'),
                                                                       ('2007','2007'),
                                                                       ('2006','2006'),
                                                                       ('2005','2005'),
                                                                       ('2004','2004'),
                                                                       ('2003','2003'),
                                                                       ('2002','2002'),
                                                                       ('2001','2001'),
                                                                       ('2000','2000'),
                                                                       ('1999','1999'),
                                                                       ('1998','1998'),
                                                                       ('1997','1997'),
                                                                       ('1996','1996'),
                                                                       ('1995','1995'),
                                                                       ('1994','1994'),
                                                                       ('1993','1993'),
                                                                       ('1992','1992'),
                                                                       ('1991','1991'),
                                                                       ('1990','1990'),
                                                                       ('1989','1989'),
                                                                       ('1988','1988'),
                                                                       ('1987','1987'),
                                                                       ('1986','1986'),
                                                                       ('1985','1985'),
                                                                       ('1984','1984'),
                                                                       ('1983','1983'),
                                                                       ('1982','1982'),
                                                                       ('1981','1981'),
                                                                       ('1980','1980'),
                                                                       ('1979','1979'),
                                                                       ('1978','1978'),
                                                                       ('1977','1977'),
                                                                       ('1976','1976'),
                                                                       ('1975','1975'),
                                                                       ('1974','1974'),
                                                                       ('1973','1973'),
                                                                       ('1972','1972'),
                                                                       ('1971','1971'),
                                                                       ('1970','1970'),
                                                                       ('1969','1969'),
                                                                       ('1968','1968'),
                                                                       ('1967','1967'),
                                                                       ('1966','1966'),
                                                                       ('1965','1965'),
                                                                       ('1964','1964'),
                                                                       ('1963','1963'),
                                                                       ('1962','1962'),
                                                                       ('1961','1961'),
                                                                       ('1960','1960'),
                                                                       ('1959','1959'),
                                                                       ('1958','1958'),
                                                                       ('1957','1957'),
                                                                       ('1956','1956'),
                                                                       ('1955','1955'),
                                                                       ('1954','1954'),
                                                                       ('1953','1953'),
                                                                       ('1952','1952'),
                                                                       ('1951','1951'),
                                                                       ('1950','1950'),]), required = False,)
        bio = forms.CharField( widget=forms.Textarea)


def clean(self):
        cleaned_data = self.cleaned_data
        usern = cleaned_data.get("usern")
        passw = cleaned_data.get("passw")
        passwr = cleaned_data.get("passwr")
        uemail = cleaned_data.get("uemail")
        firstname = cleaned_data.get("firstname")
        lastname = cleaned_data.get("lastname")
        photo = cleaned_data.get("photo")
        gender = cleaned_data.get("gender")
        day = cleaned_data.get("day")
        month = cleaned_data.get("month")
        year = cleaned_data.get("year")
        bio = cleaned_data.get("bio")
        if self.cleaned_data.get('passw') and self.cleaned_data.get('passwr') and self.cleaned_data['passw'] != self.cleaned_data['passwr']: 
                   raise ValidationError(u'Please make sure your passwords match.') 
        
        if not usern or not passw or not passwr or not uemail or not firstname or not lastname:
                raise forms.ValidationError("Please fill out all required fields!")
        # Always return the full collection of cleaned data.
        return cleaned_data
