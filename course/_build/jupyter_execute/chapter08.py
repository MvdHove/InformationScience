# Chapter 8: Library Management Systems

![](images/Brocade.png)

__[Brocade software visualization](https://anet.be/visualisering/project/hierarchical-edge-bundling.htm)__

In this chapter about the Brocade library management system (LMS) we will try to tie the previous chapters together. Above all, the aim is the illustrate the overall **architecture** of an information system, i.e. how different technologies come together to make up a system.

## Brocade Library Services

(source: __[Wikipedia](https://en.wikipedia.org/wiki/Brocade_Library_Services)__)

Brocade, in full "Brocade Library Services" is a web-based library information management system developed by the University of Antwerp (UAntwerp) in 1998 by a section of the University Library called **Anet**. Brocade is designed as a web-based application, sold via a cloud license model. The system is multilingual and uses open source components.

Brocade offers library and archival institutions a complete suite of **applications** allowing them to:

- create, maintain and publish bibliographical, archival and documentary databases;
- automate all back-office tasks in a library (cataloguing, authority control and thesaurus management, patron administration, circulation, ordering, subscription control, electronic resource management, interlibrary lending and document delivery) and an archival institution (ISAAR authorities, archival acquisitions, ISAD descriptions, descriptions of objects such as manuscripts, photos, letters, …)
- offer electronic services to the library end-users (online public access catalogue, SMS services, personalized MyLib-environment, document requests, alerting service, self-renewal, …)

The networked topology of the application lets libraries work together, share information, share catalogues, while still keeping their own identity and independency when it comes to typical local functions such as acquisition and circulation.

Brocade is a completely **web-based** application, available anywhere, anyplace and anytime (where an internet connection is available) using standard browsers such as Firefox, Internet Explorer, Safari, Opera and Chrome. Brocade does not require installation of specific clients on the user’s desktop. Installation of software on local PCs is kept to a strict minimum: a PDF reader and an application called Localweb which caters for ticket printing and provides basic circulation operations when the network fails. As the Brocade server is hosted and managed centrally, software updates and system upgrades do not require interaction from the local library staff. Brocade uses a central software repository from which bug fixes can easily be installed overnight to all Brocade systems. All new releases are also installed centrally from this repository.

Target **customers** for Brocade are libraries (public libraries, academic and education libraries, special libraries), museums, documentation centres and archival organisations. The Brocade system has been implemented in various libraries in Belgium, The Netherlands and South Africa.

## Server

It all starts with a server, a physical machine located in the University of Antwerp's server farm. It currently runs Red Hat OS and uses __[Ansible](https://www.ansible.com/)__ for application deployment and configuration management. This means we do not manually install applications, but automate the installation process and describe it in detail in (`.yaml`) configuration files. This not only saves our system engineer a lot of time, it also ensures the consistency of the installation process (correct versions of software, dependencies, installation order, ...)

The following components are key parts of our server infrastructure:

### MUMPS

__[MUMPS](https://en.wikipedia.org/wiki/MUMPS)__ (or "M") is both a key-value database and an integrated programming language (which used to be quite common). How does that work? Well, MUMPS is an interpreted language, so you have an interpreter (same as in Python) at your disposal where you can do things like this:

```M
s ^USERS(1,"first")="Tom"
s ^USERS(1,"last")="Deneire"
s ^USERS(1,"email")="deneiretom@gmail.com"
```

This instruction tells the database to define a **global variable** (the `^` caret sign makes it a global), which will be available both during the program's runtime and which will be saved to an area of physical disk space designated for these globals, making it effectively a database.

The structure is that of a subscripted array, which is equivalent to this in JSON

```json
{"USERS":
	{
		"1": {
			"email": "deneiretom@gmail.com",
			"first": "Tom",
			"last": "Deneire"
		}
	}
}
```

Of course, you can also run code from files in MUMPS. These have extension `.m` and need to be installed in a designated `r` folder (e.g. `library/mumps/brocade/r`).

There are now, and have always been, several __[MUMPS implementations](https://en.wikipedia.org/wiki/MUMPS#History)__, one of which is __[G.TM](https://en.wikipedia.org/wiki/GT.M)__. G.TM is now open source, which allows a company called __[YottaDB](https://yottadb.com/)__ to distribute it and offer database support. For Brocade, YottaDB is our database provider, but technically our MUMPS platform and compiler is G.TM.

YottaDB also provide a C and Go wrapper, so you can access the MUMPS database without using MUMPS, if you want. You see, MUMPS is a language that, like all languages, has its __[flaws](https://thedailywtf.com/articles/A_Case_of_the_MUMPS)__. On the other hand, MUMPS is simple, fast and powerful, and is codified in an __[ISO-standard](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)__ which means that is allows for very stable code to build applications that can stand the test of time.

In any case, MUMPS is the heart of Brocade: the database that records all of our data and metadata. For instance, this is how book `c:lvd:123456` which we used as an example in chapter05 is stored in our database, in global `^BCAT`:

```mumps
^BCAT("lvd",123456)="^UA-CST^53320,52220^tdeneire^65512,39826^^^"
^BCAT("lvd",123456,"au",1)="aut^0^oip^Sassen^Ferdinand^^nd"
^BCAT("lvd",123456,"co",1)="190 p.^^^^^oip^nd^normal^^^^^^^"
^BCAT("lvd",123456,"dr","paper")=""
^BCAT("lvd",123456,"ed",1)="oip^2 ed.^nd"
^BCAT("lvd",123456,"im",1)="Antwerpen^0^nd^YYYY^1932^^YYYY^^^pbl^0^Standaard^oip^nd^normal"
^BCAT("lvd",123456,"lg",1)="dut^dt"
^BCAT("lvd",123456,"lm","zebra")=""
^BCAT("lvd",123456,"nr",1)="co^0^1.248929^oip^nd^"
^BCAT("lvd",123456,"nr",2)="oclcwork^0^48674539^oip^^"
^BCAT("lvd",123456,"nr",3)="oclc^0^781576701^oip^nd^"
^BCAT("lvd",123456,"opac","cat.all","*")=""
^BCAT("lvd",123456,"opac","cat.anet","*")=""
^BCAT("lvd",123456,"opac","cat.ua","*")=""
^BCAT("lvd",123456,"pk","TPC")=""
^BCAT("lvd",123456,"pk","TPC","p:lvd:5554031")="^LZ 10/3/12^more-l^^^^^^^^^^^"
^BCAT("lvd",123456,"pk","UA-CST")=""
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205824")="^MAG-Coll 113.1/2^mag-o^^^^^^^0^^^^"
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205824","vo","-")=""
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205824","vo","-","o:lvd:261838")=""
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205825")="^FILO 19 A-SASS 32^filo-a^^^^^^^^^^^"
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205825","vo","-")=""
^BCAT("lvd",123456,"pk","UA-CST","p:lvd:205825","vo","-","o:lvd:261839")=""
^BCAT("lvd",123456,"re","lw")="1^1"
^BCAT("lvd",123456,"re","lw"," ","c:work:45740")=""
^BCAT("lvd",123456,"re","vnr")="1^1"
^BCAT("lvd",123456,"re","vnr"," 1932: 4","c:lvd:222144")=""
^BCAT("lvd",123456,"su","a::19:1")=""
^BCAT("lvd",123456,"su","a::93.001:1")=""
^BCAT("lvd",123456,"ti",1)="h^dut^1^0^oip^Geschiedenis van de wijsbegeerte der Grieken en Romeinen^^fp"
```



### Apache and PHP

Our server uses Apache webserver to host a website with a URL that ends in `?brocade.phtml`. This file is where we link up our frontend (HTML/Javascript/CSS) and backend (MUMPS).

The `p` in `brocade.phtml` stands for PHP, it is a HTML file which can also execute PHP code. PHP (unlike Javascript) runs *server side* which means it can access the server's shell. The shell can then start a MUMPS that processes the input HTML (e.g. username and password), performs a database operation (e.g. lookup access rights in the database) and then produces output HTML over stdout. This is then read by PHP again to enable the server to render it on screen again.

### Python

Our server also has a Python installation, including several (but well-chosen) third-party packages (such as `pylucene`). In Brocade, Python is used for many different things, but one of its main purposes is to run what we call **toolcat applications**.

Toolcat applications are typically pieces of specific backend software that offer support or extensions for other applications.

Some examples include:

- `mutil`: maintenance of MUMPS
- `crunch`: storage monitoring (disk space, database regions, ...)
- `musqet`: export of MUMPS data to `.sqlite`
- `docman`: file storage, e.g. images, PDFs, ...
- `lucene`: our Python wrapper (using `pylucene`) for Lucene

So if a user uses Brocade to export a dataset in .sqlite, what happens under the hood is that MUMPS goes to the shell to trigger a `musqet` command. This is then executed with Python and the result is stored on the server with `docman`. The result is offered to the user as a download link.

Over the years, Anet has also developed Python packages that are able to read data from the MUMPS database or send data to it.

### Other software

Other software installed on the server, includes Go (for systems programming, e.g. scheduling tasks such as cleaning `/library/tmp`) and Lucene for indexing.

## Qtech

All Brocade software, whether it is MUMPS, Python or what have you, is maintained in a software repository on the server (`library/software`). However, when a developer wants to interact with this repository, for instance to add or edit a file, this is not done on the server directly. There are many reasons for this. For one, this would be impractical, as it would mean that developers could not use their own tools (e.g. code editor) but whatever is present on the server (e.g. `vi`), and that all developers would be working on the same files. Secondly, it was also be dangerous, as removing the wrong file with the wrong command could result in a permanent loss of the software.

Instead local developers get a copy of the software repository on their local machine, very much like a clone from GitHub, and work on that. When they want to push their changes to the server repository, they use a toolcat application with GUI called `Qtech`. This takes care of version control, of copying the local files to their remote controle, and also of installing the software. For instance, in order to be executable by MUMPS `.m` files need to be put in a designated directory (`library/mumps/brocade/r`), which is also done by Qtech. Or, when a developer makes a new toolcat application, it needs to be available in the `$PATH` environment variable on the server. Again this is handled by Qtech.

### Registry

To do that in a clean and permanent way, we use a JSON file called `registry.json`. This file then contains keys like, `GTM-rou-dir` when stands for `library/mumps/brocade/r`. By using not the path itself, but calling the appropriate key from `registry.json` in our software, we make sure that should YottaDB ever change the location of the designated folder for M routines, we only need to change the registry key and all depending software would still run correctly.

There is also a version of `registry.json` on our local machines, which is important because of keys like `os-sep`. Sometimes Qtech or another toolcat application needs to perform a local operation on our machine (e.g. install an extension for Visual Studio Code), and in those cases it is important to know the appropriate separator for that local machine.

### Brocade object files

One of Qtech's main functions is to translate the bespoke Brocade object files we use to help our development. 

#### Macros (.d files)

Standard MUMPS code (MUMPS has an ISO standard) is kind of hardcore and limited. We code in a kind of upgrade `.m` files which are a superset of the .m files YottaDB/G.TM work with. However, in order for YottaDB/GTM to be able to compile them, they need to be translated to standard M code. For instance, one thing that needs to be translated are our **macros** (defined in `.d` files).

__[Macros](https://en.wikipedia.org/wiki/Macro_(computer_science))__ are patterns that specify how a certain input should be mapped to a replacement output. They are used to make it easy to invoke common command sequences. You see, MUMPS, being quite a minimal language, has no clean way to organize code in libraries or modules. Of course, it is possible to call code that performs, for instance, a `split` operation on a string from a MUMPS routine, but this would look like this:

```M
s string="Hello world"
s RAresult=""
d %Split^stdstring(.RAresult,string," ",1,1)
```

This is not very readable and it means you need to memorize the appropriate MUMPS routine (`stdstring.m`) and the appropriate code label (`%Split`).

With macros, however, we can use this, which is much easier to use and therefore promotes code reuse.

```M
m4_strStrip($target=RAresult, $source="string", $chars=" ", $clean=1)
```

Qtech then translates this macro to the 'pure' MUMPS version before installing the routine in the designated folder. (By the way, the `m4` in the macro name is a wink to the legendary __[m4 macro processor](https://en.wikipedia.org/wiki/M4_(computer_language))__ that is part of the POSIX standard.)

#### Screens (.x files)

Sending HTML as a string from MUMPS over stdout to the webserver probably sounds quite "bare metal", and of course it kind of is. Therefore, we have set up a few things which make frontend development much easier.

Instead of have to cobble together pieces of html in our MUMPS routines, we use **.x files** with which our .m files communicate with macros. These .x files are a superset of HTML which allows you to treat them like regular HTML files. Additionaly they grant access to the session's MUMPS variables, and also allow to interact with our own templating system.

e.g. (MUMPS session has variable `UDuser="tdeneire"`)

xfile:

```X
{UDuser|staff}
```

produces this HTML:
```html
<a href="mailto:tom.deneire@uantwerpen.be">Tom Deneire</a>
```

Again it is Qtech that translates these .x files to proper HTML to send to Apache.

#### Language codes (.l files)

Another example of Qtech's role is the way it helps Brocade to function in a multilingual environment. You see, every time we need to display information that is language-dependent, for instance, the word "Title" (which would be "Titel" in a Dutch Brocade, "Titre" in a French one, ...), we do not use the term itself, but refer to a language code that is described in an **.l file**. For instance, in `catalografie.l`

```l
lgcode Titel:
    N: «Titel»
    E: «Title»
    F: «Titre»
```

This is then translated appropriately by Qtech using the Brocade system's language setting.

#### Metainformation (.b files)

One final important aspect of what makes Brocade tick is what we call **metainformation**, recorded in .b files.

We use this word for software metadata. Good software is as generic as possible, which means that it is often better not to hard-code specific metadata in your application, but to build a metadata framework that you can address from your application.

For instance, when building an application to catalogue books you not only want to record a book's title, but also it's specific title type, e.g. main title, subtitle, genre title (e.g. the Bible), parallel title (e.g. bilingual titles), incipit, ... Now you could make a HTML select element in your form and hardcode these title types, but that's a bad idea. For instance, when you want to add a title, you have to go back to the code (perhaps in several applications!) and change the HTML. Or, when you distribute your software to serveral libraries and library A wants title types 1-5, but library B only wants title types 1-3, you need to complicate matters even more.

The correct solution is to register this metadata of title types in a database and then call that metadata from the application. That way, you can organize this information in one place and one place only. So, in Brocade, you have metainformation for title types (`menu/titlety`), recorded in the MUMPS database, but if necessary, also available for other environments (e.g. Python, Go), through regular conversion to JSON (`library/meta/json`)

So, in our software, we have a macro which constructs HTML select options with all concrete instances of this metatype for title types.

```M
m4_selectMeta(select, $type="titlety", $template="say",$default="", $lg="E", $cgonly=1)
w select
```

output:

```html
<option value='cb'>Biomed title</option>
<option value='ch'>Titel Harvard Law Review</option>
<option value='ci'>Title Index Medicus</option>
<option value='cj'>Title Judit</option>
<option value='cs'>Citeertitel ISI</option>
<option value='e'>Multiple title</option>
<option value='h'>Title</option>
<option value='ko'>Portion of title</option>
<option value='m'>Uniform title (musical works)</option>
<option value='nr'>Opus title</option>
<option value='o'>Original title</option>
<option value='p'>Parallel title</option>
<option value='rec'>Reviewed title</option>
<option value='s'>Filing title</option>
<option value='tc'>Collocation title</option>
<option value='u'>Uniform title</option>
<option value='va'>Other title</option>
```

By combining metainformation you can then further customize your application. For instance, if you make metainformation for catalography forms and record there which title types a form offers, you can make one application that offers multiple libraries their own unique way of doing catalography.

The role of Qtech in this final type of Brocade object files (.[dxlb] files) is to take the metainformation out of the .b file representation and make it available in MUMPS and in the aforementioned JSON format.

We also have special VScode extensions to format these Brocade object files.

## Production server

So far we've been speaking about 'the' server, but there are in fact several.

The one mentioned was actually the *development* server (we call it "presto"), as of course we don't code on the *production* server ("moto"). If you mess that software up, all users are affected. (There are even more servers, e.g. a demonstration server, a storage server and - importantly - a replication server)

This works like this: we are currently developing Brocade version 5.20, whereas on the production server we have Brocade version 5.10 running, which we leave untouched. When we are finished with 5.20 and want to install the new release, we basically copy the new software (filepath `library/software`) from the development server to the production server, while leaving the data (e.g. the MUMPS database) intact (filepath `library/database`). If any additional operations need to be performed to get everything running, we write release software in Python and/or MUMPS.





## Optional: YDB Acculturation Workshop

If you want a taste of what it is like to set up your own library system, you can start by getting the YDB MUMPS engine running. After all, it is open source software, which you can download for free. 

However, for a first acquaintance it's probably better to take a look at the __[YottaDB Acculturation Workshop](https://docs.yottadb.com/AcculturationGuide/acculturation.html)__ which the company has made available. This will guide you through setting up YDB in a virtual container and addressing the MUMPS database, either with MUMPS, C or Go (they are currently working on a Python wrapper).



