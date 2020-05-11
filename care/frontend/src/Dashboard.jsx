import React from 'react';
import axios from 'axios';

import {
    CircularProgress, Typography, Grid, TextField, Container,
    Checkbox, FormControlLabel, TableContainer, Table, TableHead,
    TableBody, TableRow, Input, TableCell
} from '@material-ui/core';
import MaskedInput from 'react-text-mask';


function DateInput(props) {
    let { inputRef, ...other } = props;
    return (
        <MaskedInput {...other}
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            placeholderChar={'\u2000'}
        />

    )
}

export default class Dashboard extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            error: false,
            submissions: [],
            minDate: '',
            maxDate: '',
            filterNewCases: false,
            filterCluster: false
        }

        this.handleCheckboxInput = this.handleCheckboxInput.bind(this);
        this.handleDateInput = this.handleDateInput.bind(this);
        this.fetchSubmissions = this.fetchSubmissions.bind(this);

        this.fetchSubmissions({});
    }

    handleCheckboxInput(event) {
        this.state[event.target.name] = event.target.checked;
        this.fetchSubmissions(this.state);
        this.setState({
            loading: true
        });

    }

    handleDateInput(event) {
        this.state[event.target.name] = event.target.value;
        if (!event.target.value.includes('\u2000')) {
            this.fetchSubmissions(this.state);
            this.state.loading = true;
        }
        this.setState({});
    }

    fetchSubmissions(params) {
        axios.get('/api/submissions', {
            params: {
                'date_min': params.minDate || null,
                'date_max': params.maxDate || null,
                'new_cases': params.filterNewCases || null,
                'cluster': params.filterCluster || null
            }
        }).then(res => {
            this.setState({
                loading: false,
                submissions: res.data
            });
        }).catch(error => {
            this.setState({
                loading: false,
                error: false
            });
        });
    }

    render() {
        return (
            <Container maxWidth="lg">
                <Typography variant="h4">
                    PCHD Qualtrics Submissions
                </Typography>
                <Grid container>
                    <Grid item xs={1}>
                        <Typography>Date range:</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <Input
                            value={this.state.minDate}
                            onChange={this.handleDateInput}
                            name="minDate"
                            inputComponent={DateInput}
                        />
                    </Grid>
                    <Grid item xs={1}>
                        <Typography align="center">to</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <Input
                            value={this.state.maxDate}
                            onChange={this.handleDateInput}
                            name="maxDate"
                            inputComponent={DateInput}
                        />
                    </Grid>
                </Grid>
                <Grid container>
                    <Grid item xs={1}>
                        <Typography>Filter:</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <FormControlLabel
                            control={<Checkbox
                                checked={this.state.filterNewCases}
                                onChange={this.handleCheckboxInput}
                                name="filterNewCases" />}
                            label="New Cases"
                        />
                    </Grid>
                    <Grid item xs={2}>
                        <FormControlLabel
                            control={<Checkbox
                                checked={this.state.filterCluster}
                                onChange={this.handleCheckboxInput}
                                name="filterCluster" />}
                            label="Cluster"
                        />
                    </Grid>
                    
                </Grid>
                
                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Facility</TableCell>
                                <TableCell>Address</TableCell>
                                <TableCell>Phone</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>End&nbsp;Date</TableCell>
                            </TableRow>
                        </TableHead>
                        {!this.state.loading &&
                            <TableBody>
                                {this.state.submissions.map((submission) => (
                                    <TableRow key={submission.id}>
                                        <TableCell>{submission.facility.name}</TableCell>
                                        <TableCell>{submission.facility.address}</TableCell>
                                        <TableCell>{submission.facility.phones}</TableCell>
                                        <TableCell>{submission.facility.emails}</TableCell>
                                        <TableCell>{submission.created_date}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        }
                    </Table>
                    {this.state.loading && <CircularProgress />}
                    {this.state.error &&
                        <Typography>
                            An error occurred.
                        </Typography>
                    }
                </TableContainer>
            </Container>
        )
    }
}
