            // Get the value of the input textbox
            var link = document.getElementById("linkInput").value;
            console.log(link)
            alert(link)
            // Clear the textbox
            document.getElementById("linkInput").value = "";
            // Return the link
            window.location.reload();
            out = document.getElementById("output")     
            out