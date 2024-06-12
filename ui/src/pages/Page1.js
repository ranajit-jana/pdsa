import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Select, Table, message } from 'antd';
import { createPIIEntity, getPIIEntities, updatePIIEntity } from '../api'; // Import API methods
import './Page1.css';

const { Option } = Select;
const { TextArea } = Input;

const Page1 = () => {
  const [form] = Form.useForm();
  const [dataSource, setDataSource] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedRecordKey, setSelectedRecordKey] = useState(null);

  const fetchPIIEntities = async () => {
    try {
      setLoading(true);
      const entities = await getPIIEntities();

      // Ensure that the id field exists in the entities
      const formattedEntities = entities.map((entity) => ({
        key: entity.entity_id, // Assuming the entity object has an 'id' field
        entity: entity.entity_name,
        description: entity.entity_description,
        category: entity.entity_category,
      }));

      setDataSource(formattedEntities);
      setLoading(false);
    } catch (error) {
      message.error('Failed to load PII entities');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPIIEntities();
  }, []);

  const handleFinish = async (values) => {
    try {
      if (selectedRecordKey !== null && selectedRecordKey !== undefined) {
        const entityId = parseInt(selectedRecordKey, 10);
        const updatedEntity = await updatePIIEntity(entityId, {
          entity_description: values.entity_description,
          entity_category: values.entity_category,
        });

        const updatedDataSource = dataSource.map((record) =>
          record.key === entityId
            ? {
                ...record,
                description: updatedEntity.entity_description,
                category: updatedEntity.entity_category,
              }
            : record
        );
        setDataSource(updatedDataSource);
        setSelectedRecordKey(null); // Reset selected record key after update
        message.success('PII entity updated successfully');
      } else {
        // Create new entity
        const newEntity = await createPIIEntity({
          entity_name: values.entity_name,
          entity_description: values.entity_description,
          entity_category: values.entity_category,
        });

        setDataSource([
          ...dataSource,
          {
            key: newEntity.entity_id, // Ensure the key is the id of the new entity
            entity: newEntity.entity_name,
            description: newEntity.entity_description,
            category: newEntity.entity_category,
          },
        ]);
        message.success('PII entity created successfully');
      }
      form.resetFields();
    } catch (error) {
      message.error('Failed to save PII entity');
    }
  };

  const handleCancel = () => {
    form.resetFields();
    setSelectedRecordKey(null);
  };

  const columns = [
    {
      title: 'Entity',
      dataIndex: 'entity',
      key: 'entity',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => {
        return (
          <Button type="link" onClick={() => handleEdit(record.key)}>
            Edit
          </Button>
        );
      },
    },
  ];

  const handleEdit = (key) => {
    const recordIndex = dataSource.findIndex((item) => item.key === key);
    if (recordIndex !== -1) {
      const record = dataSource[recordIndex];
      form.setFieldsValue({
        entity_name: record.entity,
        entity_description: record.description,
        entity_category: record.category,
      });
      setSelectedRecordKey(key); // Set selected record key
    }
  };

  return (
    <div>
      <h2>PII Detection and Sensitive Analyzer</h2>
      <Form form={form} layout="vertical" onFinish={handleFinish}>
        <Form.Item
          label="Entity Name"
          name="entity_name"
          rules={[{ required: true, message: 'Please select an entity name!' }]}
        >
          <Select placeholder="Select an entity name" disabled={selectedRecordKey !== null}>
            <Option value="ENTITY_NAME">ENTITY_NAME</Option>
            <Option value="PERSON">PERSON</Option>
            <Option value="PHONE_NUMBER">PHONE_NUMBER</Option>
            <Option value="EMAIL_ADDRESS">EMAIL_ADDRESS</Option>
            <Option value="ADDRESS">ADDRESS</Option>
            <Option value="AADHAR">AADHAR</Option>
            <Option value="BANK_ACCOUNT">BANK_ACCOUNT</Option>
            <Option value="CREDIT_CARD">CREDIT_CARD</Option>
            <Option value="CREDIT_CARD_CVV">CREDIT_CARD_CVV</Option>
            <Option value="CREDIT_CARD_EXPIRY_DATE">CREDIT_CARD_EXPIRY_DATE</Option>
            <Option value="DATE_OF_BIRTH">DATE_OF_BIRTH</Option>
            <Option value="MOTHERS_MAIDEN_NAME">MOTHERS_MAIDEN_NAME</Option>
            <Option value="PAN_NUMBER">PAN_NUMBER</Option>
          </Select>
        </Form.Item>
        <Form.Item
          label="Entity Category"
          name="entity_category"
          rules={[{ required: true, message: 'Please select an entity category!' }]}
        >
          <Select placeholder="Select an entity category">
            <Option value="Category1">Category1</Option>
            <Option value="Category2">Category2</Option>
            <Option value="Category3">Category3</Option>
          </Select>
        </Form.Item>
        <Form.Item
          label="Entity Description"
          name="entity_description"
          rules={[{ required: true, message: 'Please enter a description!' }]}
        >
          <TextArea rows={2} placeholder="Enter description" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
          <Button style={{ marginLeft: '10px' }} onClick={handleCancel}>
            Cancel
          </Button>
        </Form.Item>
      </Form>
      <Table columns={columns} dataSource={dataSource} loading={loading} />
    </div>
  );
};

export default Page1;
