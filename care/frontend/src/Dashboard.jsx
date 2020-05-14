import React from 'react';

import {
    Typography, Toolbar, CssBaseline,
    AppBar, makeStyles, Drawer, List, ListItem, ListItemText
} from '@material-ui/core';

import SubmissionDashboard from './SubmissionDashboard';
import FacilityDashboard from './FacilityDashboard';

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
    },    
    appBarSpacer: theme.mixins.toolbar,
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
    },
    drawer: {
        width: 200,
        flexShrink: 0,
    },
    drawerPaper: {
        width: 200,
    },
    drawerContainer: {
        overflow: 'auto',
    }
}));

export default function Dashboard() {
    const classes = useStyles();
    
    const pages = [
        {
            title: 'PCHD Facilities',
            abbr: 'Facilities',
            component: FacilityDashboard
        },
        {
            title: 'PCHD Qualtrics Submissions',
            abbr: 'Submissions',
            component: SubmissionDashboard
        }
    ];

    const [page, setPage] = React.useState(pages[0]);

    return (
        <div className={classes.root}>
            <CssBaseline />
            <AppBar className={classes.appBar}>
                <Toolbar>
                    <Typography component="h1" variant="h6" noWrap>
                        {page.title}
                    </Typography>
                </Toolbar>
            </AppBar>            
            <Drawer
                className={classes.drawer}
                variant="permanent"
                classes={{
                    paper: classes.drawerPaper,
                }}
            >
                <Toolbar />
                <div className={classes.drawerContainer}>
                    <List>
                        {pages.map(p => (
                            <ListItem button key={p.abbr} selected={page.abbr === p.abbr} onClick={() => setPage(p)}>
                                <ListItemText primary={p.abbr} />
                            </ListItem>
                        ))}
                    </List>
                </div>
            </Drawer>
            <div className={classes.appBarSpacer} />
            <page.component classes={classes}/>
        </div>
    );
}
