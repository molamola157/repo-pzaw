const liczba = document.getElementById('wynik');
        
        if (liczba < 0) {
          document.style.color = 'red';
        } 
        else if (liczba > 0) {
          document.style.color = 'green';
        }
        else {
            document.style.color = 'gray';
        }