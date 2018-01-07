import React from "react";

import {Table, Icon, Loader, Segment} from "semantic-ui-react";

import moment from "moment";


const ConfigListItem = function (props) {
    const {item: {id, name, created, validity_end, email, download_url}, onSendEmail, sending} = props;
    const relative_created = moment(created).fromNow();
    const relative_validity_end = moment(validity_end).fromNow();

    const renderSend = () => {
        if(!sending && onSendEmail) {
            return (<Icon link style={{marginRight: 16}} name='mail' onClick={() => onSendEmail(id)}/>);
        } else if(sending && onSendEmail) {
            return (
                <Loader style={{marginRight: 16}} active inline size="tiny"/>
            );
        } else {
            return("");
        }
    };

    const renderDownload = () => {
        if(download_url) {
            return (<a href={download_url}><Icon link name='download'/></a>);
        } else {
            return("");
        }
    };

    return(
        <Table.Row>
            <Table.Cell>{name}</Table.Cell>
            <Table.Cell>{relative_created}</Table.Cell>
            <Table.Cell>{relative_validity_end}</Table.Cell>
            <Table.Cell>{email}</Table.Cell>
            <Table.Cell textAlign='right'>
                {renderSend()}
                {renderDownload()}
            </Table.Cell>
        </Table.Row>
    );
};

export const ConfigList = function(props) {

    const {sending} = props;
    const items = props.items.map((item) => {
        return <ConfigListItem key={item.id}
            item={item}
            sending={sending && sending.has(item.id)}
            onSendEmail={props.onSendEmail}/>;
    });

    return(
        <Table>

            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Name</Table.HeaderCell>
                    <Table.HeaderCell>Created</Table.HeaderCell>
                    <Table.HeaderCell>Expiration</Table.HeaderCell>
                    <Table.HeaderCell>E-Mail</Table.HeaderCell>
                    <Table.HeaderCell></Table.HeaderCell>
                </Table.Row>
            </Table.Header>

            <Table.Body>
                {items}
            </Table.Body>

        </Table>
    );
};
