path_in$ = "/home/adittmer/Downloads/htk/FAVE/FAVE-align/data/" ; change this to your data location!
tier_num = 1
path_out$ = "/home/adittmer/Downloads/htk/FAVE/FAVE-align/data/" ; change this to yuor data location!

# text grids
 Create Strings as file list... filelist 'path_in$'*.TextGrid

# select each file from the textgrid string to work on one at a time
number_of_files = Get number of strings

 for t from 1 to number_of_files
	select Strings filelist
	current_file$ = Get string... t

# open the text grid and wav files
	Read from file... 'path_in$''current_file$'
	object_name$ = selected$ ("TextGrid")
	Read from file... 'path_in$''object_name$'.wav

# for counting the number of extracted intervals		
		int = 0

# find the relevant intervals
	select TextGrid 'object_name$'
	number_of_intervals = Get number of intervals... tier_num


	for i from 1 to number_of_intervals
		select TextGrid 'object_name$'
		labeliplusone$ = "0"
		labeliplustwo$ = "0"
		labeliminusone$ = "0"
		labeliminustwo$ = "0"
		labeli$ = Get label of interval... tier_num i
		if (number_of_intervals - i) > 0
			labeliplusone$ = Get label of interval... tier_num i+1
		endif
		if (number_of_intervals - (i+1)) > 0
			labeliplustwo$ = Get label of interval... tier_num i+2
		endif
		if i > 2
			labeliminusone$ = Get label of interval... tier_num i-1
		endif
		if i > 3
			labeliminustwo$ = Get label of interval... tier_num i-2
		endif
		item$ = ""
		if labeli$ == "S" or labeli$ == "SH"
			if labeli$ == "S"
				item$ = "s" 
			endif
			if item$ == "s" and labeliplusone$ == "T"
				item$ = "st"
			endif
			if item$ == "st" and labeliplustwo$ == "R"
				item$ = "str"
			endif
			if item$ == "s" and labeliplusone$ == "P"
				item$ == "sp"
			endif
			if item$ == "sp" and labeliplustwo$ == "R"
				item$ = "spr"
			endif
			if labeli$ == "SH"
				item$ = "sh"
			endif
			if item$ == "sh" and labeliplusone$ == "T"
				item$ = "sht"
			endif
			if item$ == "sht" and labeliplustwo$ == "R"
				item$ = "shtr"
			endif
			if item$ == "sh" and labeliplusone$ == "P"
				item$ == "shp"
			endif
			if item$ == "shp" and labeliplustwo$ == "R"
				item$ = "shpr"
			endif

			# word$ = get word at location of i
			# if endtime of interval i == endtime of interval for word, then note that sfinal$ = "yes", else sfinal$ = "no"
			begin = Get starting point... tier_num i
			end = Get end point... tier_num i
			dur = end-begin

			fixed_begin$ = fixed$(begin,3)
			fixed_dur$ = fixed$(dur,3)
	
			fileappend "cog_outcome.txt" 'object_name$', 'labeliminustwo$', 'labeliminusone$', 'labeli$', 'labeliplusone$', 'labeliplustwo$' 
			...'fixed_begin$', 'fixed_dur$', 



			# Measure time points one quarter, mid, three quarters.
	
	
			measure = begin + (dur /2)
	


			select Sound 'object_name$'
			# windowing
			beginS = measure - 0.05
			endS = measure + 0.05
			Extract part... 'beginS' 'endS' Hamming 1 no
			snd = selected ("Sound")
			# preemphasis filter (Nissen, 2003)
			Filter (pre-emphasis)... 100
			sndPre = selected ("Sound")
			# calculate spectrum
			To Spectrum... yes
			# extract spectral moments
			cog = Get centre of gravity... 2

			fixed_cog$ = fixed$(cog,3)
			fileappend "cog_outcome.txt" 'fixed_cog$', 'newline$'

			plus snd
			plus sndPre
			Remove
		endif
	endfor

#Clean up
	select Sound 'object_name$'
	plus TextGrid 'object_name$'
	Remove

endfor
select Strings filelist
Remove

