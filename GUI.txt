# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Food Nutrition Information Webpage"), pos = wx.DefaultPosition, size = wx.Size( 1291,775 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 80, 80, 80 ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bHeader = wx.BoxSizer( wx.HORIZONTAL )

        self.m_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Food Nutrition Experts-.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 100,100 ), 0 )
        bHeader.Add( self.m_logo, 0, wx.ALL, 10 )


        bHeader.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_title = wx.StaticText( self, wx.ID_ANY, _(u"Food Nutrition Information Webpage"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_title.Wrap( -1 )

        self.m_title.SetFont( wx.Font( 40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_title.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.m_title.SetBackgroundColour( wx.Colour( 80, 80, 80 ) )

        bHeader.Add( self.m_title, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10 )


        bHeader.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer1.Add( bHeader, 0, 0, 0 )

        bMainBody = wx.BoxSizer( wx.HORIZONTAL )

        self.m_panelFunctions = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSearchFunctions = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"Food Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText1.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

        bSearchFunctions.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 10 )

        self.m_foodSearch = wx.TextCtrl( self.m_panelFunctions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSearchFunctions.Add( self.m_foodSearch, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10 )

        self.m_nutritionRangeCheck = wx.CheckBox( self.m_panelFunctions, wx.ID_ANY, _(u"Nutrition Range Filter"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_nutritionRangeCheck.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_nutritionRangeCheck.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        bSearchFunctions.Add( self.m_nutritionRangeCheck, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10 )

        m_rangeChoiceChoices = [ _(u"Caloric Value"), _(u"Fat"), _(u"Saturated Fats"), _(u"Monounsaturated Fats"), _(u"Polyunsaturated Fats"), _(u"Carbohydrates"), _(u"Sugars"), _(u"Protein"), _(u"Dietary Fiber"), _(u"Cholesterol"), _(u"Sodium"), _(u"Water"), _(u"Vitamin A"), _(u"Vitamin B1"), _(u"Vitamin B11"), _(u"Vitamin B12"), _(u"Vitamin B2"), _(u"Vitamin B3"), _(u"Vitamin B5"), _(u"Vitamin B6"), _(u"Vitamin C"), _(u"Vitamin D"), _(u"Vitamin E"), _(u"Vitamin K"), _(u"Calcium"), _(u"Copper"), _(u"Iron"), _(u"Magnesium"), _(u"Manganese"), _(u"Phosphorus"), _(u"Potassium"), _(u"Selenium"), _(u"Zinc"), _(u"Nutrition Density") ]
        self.m_rangeChoice = wx.Choice( self.m_panelFunctions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_rangeChoiceChoices, 0 )
        self.m_rangeChoice.SetSelection( 4 )
        bSearchFunctions.Add( self.m_rangeChoice, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_rangeMin = wx.TextCtrl( self.m_panelFunctions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_rangeMin, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10 )

        self.m_staticText7 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        bSizer6.Add( self.m_staticText7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5 )

        self.m_rangeMax = wx.TextCtrl( self.m_panelFunctions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_rangeMax, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 10 )


        bSearchFunctions.Add( bSizer6, 0, wx.EXPAND|wx.TOP, 0 )

        self.m_NutritionLevelCheck = wx.CheckBox( self.m_panelFunctions, wx.ID_ANY, _(u"Nutrition Level Filter"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_NutritionLevelCheck.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_NutritionLevelCheck.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSearchFunctions.Add( self.m_NutritionLevelCheck, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        m_nutritionTypeChoices = [ _(u"Fat"), _(u"Protein"), _(u"Carbohydrates"), _(u"Sugars"), _(u"Nutrition Density") ]
        self.m_nutritionType = wx.RadioBox( self.m_panelFunctions, wx.ID_ANY, _(u"Nutrition Type"), wx.DefaultPosition, wx.DefaultSize, m_nutritionTypeChoices, 1, wx.RA_SPECIFY_COLS )
        self.m_nutritionType.SetSelection( 4 )
        self.m_nutritionType.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_nutritionType.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_nutritionType.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer7.Add( self.m_nutritionType, 0, wx.ALL, 5 )

        m_nutritionLevelChoices = [ _(u"Low"), _(u"Medium"), _(u"High") ]
        self.m_nutritionLevel = wx.RadioBox( self.m_panelFunctions, wx.ID_ANY, _(u"Nutrition Level"), wx.DefaultPosition, wx.DefaultSize, m_nutritionLevelChoices, 1, wx.RA_SPECIFY_COLS )
        self.m_nutritionLevel.SetSelection( 0 )
        self.m_nutritionLevel.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_nutritionLevel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_nutritionLevel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer7.Add( self.m_nutritionLevel, 0, wx.ALL, 5 )


        bSearchFunctions.Add( bSizer7, 0, wx.EXPAND|wx.TOP, 5 )

        self.m_searchButton = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_searchButton.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSearchFunctions.Add( self.m_searchButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_graphSwap = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Data Graphing"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_graphSwap.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSearchFunctions.Add( self.m_graphSwap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 20 )

        self.m_staticText4 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"Food Nutrition Breakdown"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_staticText4.Hide()

        bSearchFunctions.Add( self.m_staticText4, 0, wx.ALL, 10 )

        m_breakdownChoiceChoices = []
        self.m_breakdownChoice = wx.Choice( self.m_panelFunctions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_breakdownChoiceChoices, 0 )
        self.m_breakdownChoice.SetSelection( 0 )
        self.m_breakdownChoice.Hide()

        bSearchFunctions.Add( self.m_breakdownChoice, 0, wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 10 )

        bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_barGraph = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Bar Graph"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_barGraph.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_barGraph.Hide()

        bSizer22.Add( self.m_barGraph, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10 )

        self.m_pieChart = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Pie Chart"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_pieChart.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_pieChart.Hide()

        bSizer22.Add( self.m_pieChart, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10 )


        bSearchFunctions.Add( bSizer22, 0, wx.EXPAND, 5 )

        self.m_staticText5 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"Food Nutrition Comparison"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.m_staticText5.Hide()

        bSearchFunctions.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10 )

        m_comparisonPrimaryChoices = []
        self.m_comparisonPrimary = wx.Choice( self.m_panelFunctions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_comparisonPrimaryChoices, 0 )
        self.m_comparisonPrimary.SetSelection( 0 )
        self.m_comparisonPrimary.Hide()

        bSearchFunctions.Add( self.m_comparisonPrimary, 0, wx.ALL|wx.EXPAND, 10 )

        m_comparisonSecondaryChoices = []
        self.m_comparisonSecondary = wx.Choice( self.m_panelFunctions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_comparisonSecondaryChoices, 0 )
        self.m_comparisonSecondary.SetSelection( 0 )
        self.m_comparisonSecondary.Hide()

        bSearchFunctions.Add( self.m_comparisonSecondary, 0, wx.ALL|wx.EXPAND, 10 )

        self.m_compareFoods = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Compare"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_compareFoods.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_compareFoods.Hide()

        bSearchFunctions.Add( self.m_compareFoods, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.m_foodSwap = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Search Results"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_foodSwap.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_foodSwap.Hide()

        bSearchFunctions.Add( self.m_foodSwap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 20 )


        bSearchFunctions.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"Current Page: "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer14.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.m_currentPage = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_currentPage.Wrap( -1 )

        self.m_currentPage.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_currentPage.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer14.Add( self.m_currentPage, 0, wx.ALL, 5 )


        bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText10 = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"Number of Pages: "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        self.m_staticText10.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_staticText10.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer15.Add( self.m_staticText10, 0, wx.ALL, 5 )

        self.m_pageCount = wx.StaticText( self.m_panelFunctions, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_pageCount.Wrap( -1 )

        self.m_pageCount.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_pageCount.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        bSizer15.Add( self.m_pageCount, 0, wx.ALL, 5 )


        bSizer13.Add( bSizer15, 1, wx.EXPAND, 5 )


        bSearchFunctions.Add( bSizer13, 0, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_previousPage = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Previous Page"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_previousPage.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_previousPage, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer12.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_nextPage = wx.Button( self.m_panelFunctions, wx.ID_ANY, _(u"Next Page"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_nextPage.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer12.Add( self.m_nextPage, 0, wx.ALL|wx.EXPAND, 5 )


        bSearchFunctions.Add( bSizer12, 0, wx.EXPAND, 5 )


        self.m_panelFunctions.SetSizer( bSearchFunctions )
        self.m_panelFunctions.Layout()
        bSearchFunctions.Fit( self.m_panelFunctions )
        bMainBody.Add( self.m_panelFunctions, 0, wx.EXPAND |wx.ALL, 0 )

        self.m_panelContent = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panelContent.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        self.m_panelContent.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )

        bMainContent = wx.BoxSizer( wx.VERTICAL )

        self.m_dataGrid = wx.grid.Grid( self.m_panelContent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.m_dataGrid.CreateGrid( 26, 34 )
        self.m_dataGrid.EnableEditing( False )
        self.m_dataGrid.EnableGridLines( True )
        self.m_dataGrid.EnableDragGridSize( False )
        self.m_dataGrid.SetMargins( 0, 0 )

        # Columns
        self.m_dataGrid.EnableDragColMove( False )
        self.m_dataGrid.EnableDragColSize( True )
        self.m_dataGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_dataGrid.EnableDragRowSize( True )
        self.m_dataGrid.SetRowLabelSize( 0 )
        self.m_dataGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.m_dataGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bMainContent.Add( self.m_dataGrid, 1, 0, 5 )


        self.m_panelContent.SetSizer( bMainContent )
        self.m_panelContent.Layout()
        bMainContent.Fit( self.m_panelContent )
        bMainBody.Add( self.m_panelContent, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( bMainBody, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_nutritionRangeCheck.Bind( wx.EVT_CHECKBOX, self.onRangeCheck )
        self.m_NutritionLevelCheck.Bind( wx.EVT_CHECKBOX, self.onLevelCheck )
        self.m_searchButton.Bind( wx.EVT_BUTTON, self.onSearch )
        self.m_graphSwap.Bind( wx.EVT_BUTTON, self.onGraphSwap )
        self.m_barGraph.Bind( wx.EVT_BUTTON, self.onPlotBar )
        self.m_pieChart.Bind( wx.EVT_BUTTON, self.onPlotPie )
        self.m_compareFoods.Bind( wx.EVT_BUTTON, self.onCompare )
        self.m_foodSwap.Bind( wx.EVT_BUTTON, self.onSearchSwap )
        self.m_previousPage.Bind( wx.EVT_BUTTON, self.onPrevious )
        self.m_nextPage.Bind( wx.EVT_BUTTON, self.onNext )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onRangeCheck( self, event ):
        event.Skip()

    def onLevelCheck( self, event ):
        event.Skip()

    def onSearch( self, event ):
        event.Skip()

    def onGraphSwap( self, event ):
        event.Skip()

    def onPlotBar( self, event ):
        event.Skip()

    def onPlotPie( self, event ):
        event.Skip()

    def onCompare( self, event ):
        event.Skip()

    def onSearchSwap( self, event ):
        event.Skip()

    def onPrevious( self, event ):
        event.Skip()

    def onNext( self, event ):
        event.Skip()


