# Name:Gizem Ozyildirim
# Lab 1


import csv


# Decorator   
def printContainerSize(func):
    """ It is printing the container size being returned by wrapped function"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"from decorator: returning container of size {len(result)}")
        return result
        
    return wrapper

class Uni:
    ''' Represents one university with data such as rank, name, country, number of students, student/staff ratio, and top 3 fields '''
    


    def __init__(self, rank, name, country, num_students, student_staff_ratio, top_3_fields):
        """ Initializes a new instance of the Uni class with specific attributes for university ranking data. """
        
        try:
            self._rank = rank
            self._name = name.strip()
            self._country = country.strip()
            self._num_students = num_students
            self._student_staff_ratio = student_staff_ratio
            self._top_3_fields = top_3_fields
        except ValueError as e:
            print("Error: ValueError occurred!")
            


    def __str__(self):
        ''' 
        Creates a formatted string representation of the university instance, including its rank, name, country,
        number of students, student-to-staff ratio, and top academic fields.

        '''
        
        return ("{rank} {name}: {country}\n" + 
                "\tstudents: {num_students}, ratio: {student_staff_ratio}\n" +
                "\ttop fields: {top_3_fields}").format(
                    rank=self._rank, 
                    name=self._name, 
                    country=self._country,
                    num_students=self._num_students, 
                    student_staff_ratio=self._student_staff_ratio,
                    top_3_fields=", ".join(self._top_3_fields))


    @property
    def rank(self):
        ''' Returns the rank of the university as an integer. '''
        
        return self._rank


    @property
    def name(self):
        ''' Returns the name of the university as a string. '''
        
        return self._name


    @property
    def country(self):
        ''' Returns the country where the university is located as a string. '''
        
        return self._country


    @property
    def students(self):
        ''' Returns the number of students at the university as an integer. '''
        
        return self._num_students


    @property
    def student_staff_ratio(self):
        ''' Returns the student-to-staff ratio at the university as a float. '''
        
        return self._student_staff_ratio


    @property
    def top_3_fields(self):
        ''' Returns a list of the top 3 academic fields of the university. '''
        return self._top_3_fields
        
      


        
class UniRank:
    ''' Stores data for universities and provides searches '''

    # From homework: The UniRank #1
    filename='uniRanks.csv'

    # From homework: The UniRank #2
    def __init__(self, number):
        ''' Initializes a new instance of UniRank by reading university data from a CSV file. '''
        
        if number < 1:
            raise ValueError("Number of universities must be at least 1.")
        
        self._universities = []
        universities_by_country = {}

        uni_generator = self.read_universities(number)
        for (rank, name, ranking_score, country, num_students, student_staff_ratio, top_3_fields) in uni_generator:
            new_uni = Uni(rank, name, country, num_students, student_staff_ratio, top_3_fields)
            # Store universities by country
            self._universities.append(new_uni)
            if country not in universities_by_country:
                universities_by_country[country] = []
            universities_by_country[country].append(new_uni)
        
        row_count = len(self._universities)
        optional_msg = ""
        if number > row_count:
            optional_msg = f"(only {row_count} available out of the {number} requested)"
            
        print(f"The number of universities read in: {row_count} {optional_msg}")
        print(f"The number of universities for each country:")
        
        sorted_by_uni_count = sorted(universities_by_country.items(), key=lambda item: len(item[1]), reverse=True) 
        for country_name, uni_list in sorted_by_uni_count:
            print(f"\t {country_name}: {len(uni_list)}" )
        

    
    def read_universities(self, number):
        ''' 
        Generator function that reads university data from a CSV file and 
        yields each university's data as a tuple. 
        '''
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i >= number:
                        break

                    try:
                        rank = int(row[0].strip())
                        name = row[1].strip()
                        ranking_score = row[2].strip()
                        country = row[3].strip()
                        num_students = int(row[4].strip())
                        student_staff_ratio = float(row[5].strip())
                        top_3_fields = row[6].split(',')[:3]
                    except ValueError as e:
                        break
                    
                    yield rank, name, ranking_score, country, num_students, student_staff_ratio, top_3_fields

        except FileNotFoundError:
            print(f"The {self.filename} file doesn't exist.")
            raise SystemExit(1)               

            
    # From homework: The UniRank #4
    @printContainerSize
    def getUnies(self):
        ''' Retrieves the list of all universities currently loaded into the UniRank object. '''
        
        return self._universities

    # From homework: The UniRank #5
    @printContainerSize
    def get_all_unies_by_country(self, country):
        '''Filters and returns a list of all universities from a specific country.'''
        
        unis_by_country = filter(lambda uni: uni.country.lower() == country.lower(), self._universities)
        return list(unis_by_country)
    
    # From homework: The UniRank #6
    @printContainerSize
    def sort_unis_by_criterion(self, criterion, num_of_unis):
        ''' The given criterion can be students or ratio. 
            The choice students refers to the students attribute and
            ratio refers to the student_staff_ratio attribute in the Uni class 
            '''
        num_of_unis = int(num_of_unis)
        if num_of_unis < 1:
            raise ValueError(f"The parameter num_of_unis should be at least 1. ")
        
        def student_func(item):
            return item.students
        
        def ratio_func(item):
            return item.student_staff_ratio
        
        criterion_to_property_map = {
            "students": student_func,
            "ratio": ratio_func
        }
        
        if criterion not in criterion_to_property_map.keys():
            raise ValueError(f"Invalid criterion {criterion}. Valid criteria options are {criterion_to_property_map.keys()}")
        
        sorted_unis = sorted(self._universities, key=lambda uni_item: criterion_to_property_map[criterion](uni_item), reverse=True)
        # sorted_unis = sorted(self._universities, key=lambda uni_item: student_func(uni_item), reverse=True)
        # sorted_unis = sorted(self._universities, key=lambda uni_item: uni_item.students, reverse=True)
        return sorted_unis[:num_of_unis]
        
        

            
def main():
    """
    Main function to execute the logic.
    
    """
    
    unirank = UniRank(15)
    
    lookup_table = {
        'a': unirank.getUnies,
        'c': unirank.get_all_unies_by_country,
        's': unirank.sort_unis_by_criterion
    }

    test_file = "testcases.csv"

    
    with open(test_file, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            print(f"\nTest case: {', '.join(row)}")
            test_type = row[0]
            params = row[1:]
            result = lookup_table[test_type](*params)
            if len(result) == 0:
                print("no data available")
            else:
                for uni_details in result:
                    print(uni_details)
                    
                    
    r = UniRank(300)

# main block
# 
# print("Get all unis in United States")
# print(f"{r.get_all_unies_by_country('United States')}")
# # print(a)

# print("Sort by students")
# print(f"\t{r.sort_unis_by_criterion('students', 10)}")
# print("Sort by ratio")
# print(f"\t{r.sort_unis_by_criterion('ratio', 5)}")
    
main()

'''
Manual test cases(During debugging local tests):

print("Get all unis in United States")

print(f"{r.get_all_unies_by_country('United States')}")

print("Sort by students")

print(f"\t{r.sort_unis_by_criterion('students', 10)}")

print("Sort by ratio")

print(f"\t{r.sort_unis_by_criterion('ratio', 5)}")


'''